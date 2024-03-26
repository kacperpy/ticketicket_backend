from celery import shared_task
from ticket.models import TicketSearch
from django_celery_beat.models import PeriodicTask
from ticket.tasks.scraper import create_email_message, find_best_value_ticket, extract_title, extract_ticket_values, extract_website_content, notify_via_email


@shared_task
def update_ticket_search_title(ticket_search_uuid):
    ticket_search = TicketSearch.objects.get(uuid=ticket_search_uuid)
    website_content = extract_website_content(ticket_search.url)
    title = extract_title(website_content)

    ticket_search.name = title
    ticket_search.save()

    return f"Updated name to {title}, for Ticket Search {ticket_search_uuid}."


@shared_task
def search_for_ticket(ticket_search_id):
    ticket_search = TicketSearch.objects.get(id=ticket_search_id)
    periodic_task = ticket_search.periodic_task
    website = extract_website_content(ticket_search.url)
    ticket_values_list = extract_ticket_values(website)
    desired_values = {
        "min_availability": int(ticket_search.min_availability),
        "price_threshold": float(ticket_search.price_threshold)
    }
    ticket_found = find_best_value_ticket(
        ticket_values_list,
        desired_values
    )
    ticket_data = {
        "event_name": ticket_search.name,
        "price_threshold": ticket_search.price_threshold,
        "min_availability": ticket_search.min_availability,
        "price_found": ticket_found["price"],
        "availability_found": ticket_found["availability"],
        "ticket_url": ticket_search.url

    }

    if ticket_found is not None:
        notify_via_email(
            ticket_search.created_by.email,
            create_email_message(ticket_data)
        )

        periodic_task.enabled = False
        periodic_task.save()

        return f"Ticket with price: {
            ticket_found["price"]
        } and availability: {
            ticket_found["availability"]
        } was found | Task has been disabled |"

    return "No ticket was found."
