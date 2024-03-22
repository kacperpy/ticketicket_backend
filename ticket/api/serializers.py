from rest_framework import serializers
from django_celery_beat.models import PeriodicTask
from ticket.models import TicketSearch


class PeriodicTaskReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = [
            'name',
            'task'
        ]


class PeriodicTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = [
            'name',
            'task',
            'interval',
            'expires'
        ]


class TicketSearchCreateSerializer(serializers.ModelSerializer):
    periodic_task = PeriodicTaskCreateSerializer()

    class Meta:
        model = TicketSearch
        fields = [
            'url',
            'price_threshold',
            'min_availability',
            'periodic_task'
        ]


class TicketSearchReadSerializer(serializers.ModelSerializer):
    periodic_task = PeriodicTaskReadSerializer(read_only=True)

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
            'min_availability',
            'periodic_task'
        ]
