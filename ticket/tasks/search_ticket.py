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
def search_for_ticket(price_threshold, ticket_url, min_availability, periodic_task_id):
    periodic_task = PeriodicTask.objects.get(id=periodic_task_id)
    website = extract_website_content(ticket_url)
    ticket_values_list = extract_ticket_values(website)
    desired_values = {
        "min_availability": int(min_availability),
        "price_threshold": float(price_threshold)
    }
    ticket_found = find_best_value_ticket(
        ticket_values_list,
        desired_values
    )
    ticket_data = {
        "event_name": periodic_task.ticket_searched.name,
        "price_threshold": price_threshold,
        "min_availability": min_availability,
        "price_found": ticket_found["price"],
        "availability_found": ticket_found["availability"],
        "ticket_url": ticket_url

    }
    if ticket_found is not None:
        # notify via email
        notify_via_email(
            periodic_task.ticket_searched.created_by.email,
            create_email_message(ticket_data)
        )
        # disable task
        periodic_task.enabled = False
        periodic_task.save()
        return f"Ticket with price: {
            ticket_found["price"]
        } and availability: {
            ticket_found["availability"]
        } was found | Task has been disabled |"
    return "No ticket was found."
