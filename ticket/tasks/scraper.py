import requests
from bs4 import BeautifulSoup
import re


# returns the content of the whole page
def get_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

        return None


# returns the title text of the scraped site
def extract_title(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    title_text = soup.title.text if soup.title else "Title tag not found"

    return title_text


# returns a list of objects like this: [{availability: integer, price: float}, ...]
def find_ticket_values(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    tickets_table = soup.find("table", id="ticket-list")
    ticket_values_list = []

    if tickets_table:
        number_pattern = re.compile(r'\d+')
        decimal_pattern = re.compile(r'\d+,\d+')
        rows = tickets_table.find(
            "tbody"
        ).find_all(
            "tr"
        ) if tickets_table.find("tbody") else []

        for row in rows:
            availability_tag = row.find("td", class_="availability")
            price_tag = row.find("td", class_="price")

            if availability_tag and price_tag:
                availability_match = number_pattern.search(
                    availability_tag.text
                )
                availability = int(
                    availability_match.group()
                ) if availability_match else None

                price_match = decimal_pattern.search(
                    price_tag.text.replace('.', ',')
                )
                price = float(
                    price_match.group().replace(
                        ',', '.'
                    )
                ) if price_match else None

                if availability is not None and price is not None:
                    ticket_values_list.append(
                        {"availability": availability, "price": price}
                    )

    return ticket_values_list
