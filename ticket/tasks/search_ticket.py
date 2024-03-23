from celery import shared_task
from ticket.models import TicketSearch
from ticket.tasks.scraper import extract_title, get_website_content


@shared_task
def update_ticket_search_title(ticket_search_uuid):
    ticket_search = TicketSearch.objects.get(uuid=ticket_search_uuid)
    website_content = get_website_content(ticket_search.url)
    title = extract_title(website_content)

    ticket_search.name = title
    ticket_search.save()

    return f"Updated name to {title}, for Ticket Search {ticket_search_uuid}."


@shared_task
def search_for_ticket(price_threshold, ticket_url, min_availability):
    return f"{price_threshold} {ticket_url} {min_availability}"
