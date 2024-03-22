from rest_framework import serializers

from ticket.models import TicketSearch


class TicketSearchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketSearch
        fields = [
            'name',
            'url',
            'price_threshold',
            'min_availability'
        ]


class TicketSearchReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketSearch
        fields = [
            'uuid',
            'created_at',
            'updated_at',
            'created_by',
            'name',
            'url',
            'price_threshold',
            'min_availability'
        ]
