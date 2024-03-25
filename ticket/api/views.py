import json
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ticket.api.serializers import TicketSearchCreateSerializer, TicketSearchReadSerializer
from ticket.core.constants import GENERAL_EVENT_NAME
from ticket.models import TicketSearch
import ticket.tasks.search_ticket as tasks


class TicketSearchViewSet(viewsets.ModelViewSet):
    queryset = TicketSearch.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        request_user = self.request.user
        periodic_task_name = f"{request_user.username}'s search | {
            request_user.created_searches.count() + 1}"

        ticket_search = serializer.save(
            created_by=request_user,
            name=GENERAL_EVENT_NAME
        )
        periodic_task = ticket_search.periodic_task
        periodic_task.name = periodic_task_name
        periodic_task.args = json.dumps(
            [
                str(ticket_search.price_threshold),
                ticket_search.url,
                ticket_search.min_availability,
                periodic_task.id
            ]
        )
        periodic_task.save()

        # scheduling a one time task to change the SearchTitle object name
        tasks.update_ticket_search_title.delay(ticket_search.uuid)

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketSearchCreateSerializer
        else:
            return TicketSearchReadSerializer
