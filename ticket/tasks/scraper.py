import requests
from bs4 import BeautifulSoup


def get_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes

        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def extract_title(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    title_text = soup.title.text if soup.title else "Title tag not found"

    return title_text
