from celery import shared_task
from ticket.models import TicketSearch
from django.contrib.auth import get_user_model
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


@shared_task
def update_search_title(ticket_search_uuid):
    ticket_search = TicketSearch.objects.get(uuid=ticket_search_uuid)
    website_content = get_website_content(ticket_search.url)
    title = extract_title(website_content)

    ticket_search.name = title
    ticket_search.save()

    return f"Updated name to {title}, for Ticket Search {ticket_search_uuid}."


@shared_task
def search_for_ticket(price_threshold, ticket_url, min_availability):
    return f"{price_threshold} {ticket_url} {min_availability}"
