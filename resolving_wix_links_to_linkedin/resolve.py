import pandas as pd
import requests
from urllib.parse import urlparse

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
    return resolve_redirect_link(url)

# Read the CSV file
input_csv_path = 'data/deduplicated_data.csv'
df = pd.read_csv(input_csv_path, dtype={'LinkedIn Profile': str})

# Resolve Wix redirect links safely
df['LinkedIn Profile'] = df['LinkedIn Profile'].apply(safe_resolve_redirect_link)

# Deduplicate the DataFrame using the 'Email' field
df_deduplicated = df.drop_duplicates(subset='Email')

# Save the updated and deduplicated data to a new CSV file
output_csv_path_updated = 'path_to_your_output_csv.csv'
df_deduplicated.to_csv(output_csv_path_updated, index=False)
