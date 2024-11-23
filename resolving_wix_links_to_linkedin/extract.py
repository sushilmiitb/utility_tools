import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time
import csv


# Function to resolve Wix redirect links
def resolve_redirect_link(url):
    try:
        response = requests.get(url, allow_redirects=True)
        return response.url
    except requests.RequestException:
        return url


# Function to check if a URL is a Wix redirect link
def is_wix_redirect(url):
    parsed_url = urlparse(url)
    return 'wix' in parsed_url.netloc.lower()


# Function to handle missing or empty URLs and resolve Wix redirects
def safe_resolve_redirect_link(url):
    if pd.isna(url) or not is_wix_redirect(url):
        return url
    resolved_url = resolve_redirect_link(url)
    print(f"Resolved URL: {resolved_url}")
    return resolved_url


# Function to extract last company and designation from a LinkedIn profile
def extract_linkedin_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the sections containing the experience information
        experience_section = soup.find('section', {'id': 'experience-section'})

        if experience_section:
            # Extract the last job title and company name
            last_job = experience_section.find('li')
            if last_job:
                designation = last_job.find('h3').get_text(strip=True)
                company = last_job.find('p', {'class': 'pv-entity__secondary-title'}).get_text(strip=True)
                return company, designation

        return None, None
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None, None


# Read the CSV file
input_csv_path = 'data/resolved_linkedin_urls.csv'
df = pd.read_csv(input_csv_path, dtype={'LinkedIn Profile': str})

# Output CSV file
output_csv_path = 'data/scrapped.csv'

# Ensure the output file is empty
open(output_csv_path, 'w').close()

# Write the header to the output file
with open(output_csv_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['LinkedIn Profile', 'Last Company', 'Designation'])

# Loop through the URLs and extract data
for index, row in df.iterrows():
    url = row['LinkedIn Profile']

    # Extract the information
    company, designation = extract_linkedin_info(url)

    # Print the result
    print(f"URL: {url}")
    print(f"Last Company: {company}")
    print(f"Designation: {designation}")
    print("-" * 40)

    # Write the result to the output file
    with open(output_csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([url, company, designation])

    # Introduce a random delay between 5 to 15 seconds
    time.sleep(random.randint(5, 15))
