from celery import shared_task
from ticket.models import TicketSearch
from django.contrib.auth import get_user_model


@shared_task
def test_create_ticket_search(request_user_id):
    User = get_user_model()
    created_ticket_search = TicketSearch(
        created_by=User.objects.get(id=request_user_id),
        name='test search celery',
        url='test url',
        price_threshold=99.99,
        min_availability=2
    )
    created_ticket_search.save()

    return f"created ticket search: {created_ticket_search.uuid}"
