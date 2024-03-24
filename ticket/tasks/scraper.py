import requests
from bs4 import BeautifulSoup
import re


# returns the content of the whole page
def extract_website_content(url):
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
def extract_ticket_values(html_content):
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


# checks if provided tickets have acceptable values and returns the cheapest option
def find_best_value_ticket(ticket_values_list, desired_values):
    best_ticket_values = {
        "availability": desired_values["min_availability"],
        "price": desired_values["price_threshold"]
    }
    ticket_found = False

    for ticket_values in ticket_values_list:
        if ticket_values["availability"] >= best_ticket_values["availability"] and ticket_values["price"] <= best_ticket_values["price"]:
            best_ticket_values["price"] = ticket_values["price"]
            best_ticket_values["availability"] = ticket_values["availability"]
            ticket_found = True

    return best_ticket_values if ticket_found else None
