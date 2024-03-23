import psycopg2
import json
import requests
from itertools import cycle

# Load GitHub tokens from a file and prepare them for cycling
def load_tokens():
    with open('tokens.txt', 'r') as file:
        tokens = [line.strip() for line in file]
    return cycle(tokens)

# Function to fetch repositories for a given owner from GitHub's API
def fetch_repos_for_owner(owner, tokens):
    url = f"https://api.github.com/users/{owner}/repos"
    headers = {'Authorization': f'token {next(tokens)}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [repo['name'] for repo in response.json()]
    else:
        print(f"Error fetching repos for owner {owner}: {response.status_code}")
        return []

# PostgreSQL connection parameters
conn_params = {
    "host": "localhost",
    "port": "5432",
    "database": "eclipseoss",
    "user": "swatisinghvi",
    "password": "pass1234"  
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()

# Execute query to fetch project names, technologies, and GitHub repo links
cursor.execute("""
SELECT technology, project_name, github_repo_link
FROM eclipse_projects
""")

# Fetch all the rows from the query
rows = cursor.fetchall()

# Close the database connection
conn.close()

# Load GitHub tokens
tokens = load_tokens()

# Initialize a dictionary to hold the structured data
technology_to_projects = {}

# Process each row in the fetched data
for technology, project_name, github_repo_link in rows:
    if technology not in technology_to_projects:
        technology_to_projects[technology] = {}
    if project_name not in technology_to_projects[technology]:
        technology_to_projects[technology][project_name] = []

    # Check if the GitHub repo link is "N/A" or an owner name
    if github_repo_link == "N/A":
        continue
    elif '/' not in github_repo_link:
        # Fetch all repos for the owner and append them
        repo_names = fetch_repos_for_owner(github_repo_link, tokens)
        technology_to_projects[technology][project_name].extend(repo_names)
    else:
        # Process normally for specific repos
        repo_links = [link.strip() for link in github_repo_link.split(',')]
        repo_names = [link.split('/')[-1] for link in repo_links if '/' in link] or repo_links
        technology_to_projects[technology][project_name].extend(repo_names)

# Write the structured data to a JSON file
with open('project_names.json', 'w') as json_file:
    json.dump(technology_to_projects, json_file, indent=2)
