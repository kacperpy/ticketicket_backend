from rest_framework import status, viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from ticket.api.serializers import TicketSearchCreateSerializer, TicketSearchReadSerializer
from ticket.models import TicketSearch
from ticket.tasks.search_ticket import test_create_ticket_search


class TicketSearchViewSet(viewsets.ModelViewSet):
    queryset = TicketSearch.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    # for testing celery
    def perform_create(self, serializer):
        request_user = self.request.user

        test_create_ticket_search.delay(request_user.id)

        serializer.save(
            created_by=request_user
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketSearchCreateSerializer
        elif self.action in ['list', 'retrieve']:
            return TicketSearchReadSerializer
