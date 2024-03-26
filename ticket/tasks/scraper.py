from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
from bs4 import BeautifulSoup
import re

from secret import EMAIL_SENDER, EMAIL_SENDER_SECRET_PASSWORD


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


def create_email_message(ticket_data):
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                color: #333;
            }}
            .container {{
                background-color: #f2f2f2;
                border-radius: 5px;
                padding: 20px;
            }}
            h1 {{
                color: #0275d8;
            }}
            .info {{
                margin-bottom: 12px;
            }}
            .highlight {{
                color: #d9534f;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Ticket Alert: {ticket_data['event_name']}</h1>
            <p class="info">We found tickets that match your criteria!</p>
            <p class="info">Desired Price: <span class="highlight">PLN {ticket_data['price_threshold']}</span></p>
            <p class="info">Minimum Availability: <span class="highlight">{ticket_data['min_availability']}</span></p>
            <p class="info">Price Found: <span class="highlight">PLN {ticket_data['price_found']}</span></p>
            <p class="info">Availability Found: <span class="highlight">{ticket_data['availability_found']}</span></p>
            <p class="info">Link to Ticket: <span class="highlight">{ticket_data['ticket_url']}</span></p>
        </div>
    </body>
    </html>
    """
    return html_message


def notify_via_email(recipient, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(EMAIL_SENDER, EMAIL_SENDER_SECRET_PASSWORD)

        email = MIMEMultipart('alternative')
        email['From'] = 'TickeTicket'
        email['To'] = recipient
        email['Subject'] = 'GOOD NEWS - Event ticket was found!'
        email.attach(MIMEText(message, 'html'))

        server.send_message(email)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()
