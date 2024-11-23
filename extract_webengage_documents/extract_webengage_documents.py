import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup

# Define the main URL and the directory to store the pages
MAIN_URL = "https://knowledgebase.webengage.com/docs/preface"
SAVE_DIR = "data"
START_URL = "https://knowledgebase.webengage.com/docs/dynamic-email-templating-drag-drop-editor"

# Create the save directory if it doesn't exist
os.makedirs(SAVE_DIR, exist_ok=True)

# Initialize Selenium WebDriver (assumes ChromeDriver is in your PATH)
driver = webdriver.Chrome()


def fetch_article_text(url):
    """
    Fetches the text content within the <article id="content"> section of a given URL.
    :param url: URL of the webpage to fetch
    :return: Rendered text content within the specified <article> if successful, else None
    """
    try:
        driver.get(url)
        time.sleep(2)  # Wait for JavaScript to execute and content to load
        # Parse the page source to find the <article> content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        article = soup.find('article', class_='rm-Article', id='content')
        if article:
            article_text = article.get_text(separator='\n', strip=True)
            return article_text
        else:
            print(f"No article content found in {url}")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_navbar_links(html):
    """
    Extracts all the links from the navbar with id 'hub-sidebar'.
    :param html: HTML content of the main page
    :return: List of tuples containing link text and URL
    """
    soup = BeautifulSoup(html, 'html.parser')
    navbar = soup.find('nav', id='hub-sidebar')
    links = []

    # If navbar exists, find all <a> tags within it, even if nested
    if navbar:
        for link in navbar.find_all('a', href=True):
            span = link.find('span')
            if span:
                link_text = span.get_text(strip=True)
                link_url = link['href']
                if link_url.startswith('/'):
                    link_url = "https://knowledgebase.webengage.com" + link_url
                links.append((link_text, link_url))

    return links


def save_text_content(title, content):
    """
    Saves the text content of a page.
    :param title: Title of the page (used as filename)
    :param content: Rendered text content of the page
    """
    # Sanitize title to use as a filename
    filename = os.path.join(SAVE_DIR, f"{title}.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Saved: {filename}")


def download_all_navbar_links(start_url=None, limit=3):
    """
    Main function to download the rendered text content of linked pages starting from a specified URL.
    :param start_url: URL to start downloading from (if None, starts from the beginning)
    :param limit: Number of pages to download for testing
    """
    # Step 1: Get the main page HTML using Selenium for dynamic content
    driver.get(MAIN_URL)
    time.sleep(2)
    main_page_html = driver.page_source

    # Step 2: Extract links from the navbar
    links = extract_navbar_links(main_page_html)
    print(f"Found {len(links)} links in the navbar.")

    # Step 3: Start downloading from the specified start_url
    start_downloading = start_url is None
    count = 0

    for title, url in links:
        # Skip links until we reach start_url
        if not start_downloading:
            if url == start_url:
                start_downloading = True
            else:
                continue

        if count >= limit:
            break

        # Fetch and save the article text for the current link
        article_text = fetch_article_text(url)
        if article_text:
            save_text_content(title, article_text)
            count += 1
        time.sleep(2)  # Adding a 2-second delay after each download


# Run the script starting from the specified URL with a limit of 3 pages
download_all_navbar_links(start_url=START_URL, limit=300)

# Close the Selenium WebDriver after scraping
driver.quit()
