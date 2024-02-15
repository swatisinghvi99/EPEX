import requests
from bs4 import BeautifulSoup
import psycopg2
import json

# Database connection details
db_config = {
    "host": "localhost",
    "port": "5432",
    "database": "swatis",
    "user": "swatisinghvi",
    "password": ""
}

def create_table():
    # Connect to the newly created database to create the table
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS eclipse_projects (
            id SERIAL PRIMARY KEY,
            project_name VARCHAR(255),
            project_url VARCHAR(255),
            technology VARCHAR(255),
            state VARCHAR(255),
            releases TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_project(conn, project_name, project_url, technology, state, releases):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO eclipse_projects (project_name, project_url, technology, state, releases)
            VALUES (%s, %s, %s, %s, %s)
        """, (project_name, project_url, technology, state, releases))
    conn.commit()


def scrape_additional_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract Technology
    tech = soup.find("li", class_="ellipsis hierarchy-1")
    technology_1 = tech.find("a").text if tech else "N/A" 
    if technology_1 != "Eclipse Project":
        technology = technology_1.replace("Eclipse", "").replace("Project", "").replace("®","").strip()
    else:
        technology = technology_1

    # Extract State
    state_div = soup.find("div", class_="field-name-field-state")
    state = state_div.find("div", class_="field-item").text.strip() if state_div else "N/A"

    # Extract Releases
    releases_url = url + "/governance"
    response = requests.get(releases_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    releases_div = soup.find("div", class_="field-name-field-releases")
    if releases_div:
        for row in releases_div.find_all("tr")[1:]:  # Skip header row
            cols = row.find_all("td")
            release_name = cols[0].text.strip()
            release_url = "https://projects.eclipse.org" + cols[0].find("a")["href"].strip()
            release_date = cols[1].text.strip()
            data.append({"name": release_name, "url": release_url, "date": release_date})
    else:
        # If no Releases, scrape Reviews
        reviews_div = soup.find("div", class_="field-name-field-project-reviews")
        if reviews_div:
            for row in reviews_div.find_all("tr")[1:]:  # Skip header row
                cols = row.find_all("td")
                review_name = cols[0].text.strip()
                review_url = "https://projects.eclipse.org" + cols[0].find("a")["href"].strip()
                review_date = cols[1].text.strip()
                data.append({"name": review_name, "url": review_url, "date": review_date})

    # Convert data to JSON string
    releases_or_reviews_json = json.dumps(data)

    return technology, state, releases_or_reviews_json

def scrape_projects_and_store(base_url, total_pages, conn):
    for page in range(total_pages):
        if page == 0:
            url = base_url
        else:
            url = f"{base_url}?page={page}"
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for project_div in soup.find_all("div", class_="project-teaser-body"):
            project_name = project_div.find("h4").text.replace("™","").replace("®","").strip()
            project_url = "https://projects.eclipse.org" + project_div.find("a")["href"] 
            technology, state, releases = scrape_additional_info(project_url)
            insert_project(conn, project_name, project_url, technology, state, releases)

try:
    # Create table
    create_table()
    
    # Connect to the database
    conn = psycopg2.connect(**db_config)
    
    # Base URL and total number of pages
    base_url = "https://projects.eclipse.org/list-of-projects"
    total_pages = 22
    
    print("Scraping Project Data")
    scrape_projects_and_store(base_url, total_pages, conn)
finally:
    conn.close()

print("Scraping completed. Successfully stored in database.")
