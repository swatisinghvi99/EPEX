import requests
from bs4 import BeautifulSoup
import psycopg2
import json
import time

# Database connection details
db_config = {
    "host": "localhost",
    "port": "5432",
    "database": "eclipseoss",
    "user": "swatisinghvi",
    "password": "pass1234"  
}
def make_request_with_backoff(url, max_attempts=5):
    attempt = 0
    delay = 1 

    while attempt < max_attempts:
        try:
            response = requests.get(url)
            if response.status_code // 100 == 2:
                return response
            else:
                print(f"Request failed with status code {response.status_code}. Retrying...")
                raise Exception("Request failed")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
            attempt += 1
            delay *= 2  

    raise Exception("Max attempts reached, request failed.")

def create_table():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS eclipse_projects (
            id SERIAL PRIMARY KEY,
            project_name VARCHAR(255),
            project_url VARCHAR(255),
            technology VARCHAR(255),
            state VARCHAR(255),
            github_repo_link TEXT,
            releases TEXT,
            mail_name TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_project(conn, project_name, project_url, technology, state, github_repo_link, releases, mail_name):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO eclipse_projects (project_name, project_url, technology, state, github_repo_link, releases, mail_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (project_name, project_url, technology, state, github_repo_link, releases, mail_name))
    conn.commit()


def scrape_additional_info(url):
    response = make_request_with_backoff(url)
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
    response = make_request_with_backoff(releases_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    releases_div = soup.find("div", class_="field-name-field-releases")
    if releases_div:
        for row in releases_div.find_all("tr")[1:]: 
            cols = row.find_all("td")
            release_name = cols[0].text.strip()
            release_url = "https://projects.eclipse.org" + cols[0].find("a")["href"].strip()
            release_date = cols[1].text.strip()
            data.append({"name": release_name, "url": release_url, "date": release_date})
    else:
        # If no Releases, scrape Reviews
        reviews_div = soup.find("div", class_="field-name-field-project-reviews")
        if reviews_div:
            for row in reviews_div.find_all("tr")[1:]:  
                cols = row.find_all("td")
                review_name = cols[0].text.strip()
                review_url = "https://projects.eclipse.org" + cols[0].find("a")["href"].strip()
                review_date = cols[1].text.strip()
                data.append({"name": review_name, "url": review_url, "date": review_date})

    # Convert data to JSON string
    releases_or_reviews_json = json.dumps(data)

    # Extract mailing-list name
    mailing_list_url = url+"/developer"
    response = make_request_with_backoff(mailing_list_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mailing_list_links = soup.select('a[href*="mailman/listinfo"], a[href*="mailing-list"]')

    if mailing_list_links:
        mailing_list_link = mailing_list_links[0]
        mailing_list_url = mailing_list_link.get("href")
        mailing_list_name = mailing_list_url.split('/')[-1] if mailing_list_url else "N/A"
    else:
        mailing_list_name = "N/A"
    
    github_reposs_str = "N/A"
    
    github_section = soup.find('div', class_='field-name-field-project-github-org')

    if not github_section:
        github_section = soup.find('div', class_='field-name-field-project-github-repos')

    if github_section:
        github_reposs = github_section.select('a[href*="github.com"]')
        github_reposs_str = ", ".join(link.get('href') for link in github_reposs)
        github_reposs_str = github_reposs_str.replace('https://github.com/','')

    return technology, state, github_reposs_str, releases_or_reviews_json, mailing_list_name

def scrape_projects_and_store(base_url, total_pages, conn):
    for page in range(total_pages):
        if page == 0:
            url = base_url
        else:
            url = f"{base_url}&page={page}"
        
        response = make_request_with_backoff(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for project_div in soup.find_all("div", class_="project-teaser-body"):
            project_name = project_div.find("h4").text.replace('™','').replace('®','').replace('Eclipse ','').replace('Jakarta ','').replace('LocationTech ','').strip()
            project_url = "https://projects.eclipse.org" + project_div.find("a")["href"] 
            technology, state, github_repo_link, releases, mail_name = scrape_additional_info(project_url)
            insert_project(conn, project_name, project_url, technology, state, github_repo_link, releases, mail_name)

        print(f"Stored all projects from page {page}")

try:
    create_table()
    conn = psycopg2.connect(**db_config)
    base_url = "https://projects.eclipse.org/list-of-projects?combine=&field_project_techology_types_tid=All&field_state_value_2=All&field_archived_projects%5Barchived%5D=archived"
    total_pages = 31
    
    print("Scraping Project Data")
    scrape_projects_and_store(base_url, total_pages, conn)
finally:
    conn.close()

print("Scraping completed. Successfully stored in database.")
