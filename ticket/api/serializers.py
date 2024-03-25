from rest_framework import serializers
from django_celery_beat.models import PeriodicTask, IntervalSchedule, PERIOD_CHOICES
from ticket.api.validators.validators_ticket_search import validate_if_url_allowed
from ticket.core.constants import ALEBILET_URL, TICKET_SCRAPER_TASK
from ticket.models import TicketSearch
from ticket.core.tools import get_formatted_date


class IntervalScheduleCreateSerializer(serializers.ModelSerializer):
    period = serializers.ChoiceField(choices=PERIOD_CHOICES)

    class Meta:
        model = IntervalSchedule
        fields = [
            'every',
            'period'
        ]

    def create(self, validated_data):
        interval_schedule, created = IntervalSchedule.objects.get_or_create(
            **validated_data)
        return interval_schedule


class IntervalScheduleReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = [
            'every',
            'period'
        ]


class PeriodicTaskReadSerializer(serializers.ModelSerializer):
    interval = IntervalScheduleReadSerializer(read_only=True)
    expires = serializers.SerializerMethodField()

    class Meta:
        model = PeriodicTask
        fields = [
            'name',
            'task',
            'interval',
            'expires'
        ]

    def get_expires(self, instance):
        return get_formatted_date(instance.expires) if instance.expires is not None else None


class PeriodicTaskCreateSerializer(serializers.ModelSerializer):
    interval = IntervalScheduleCreateSerializer()

    class Meta:
        model = PeriodicTask
        fields = [
            'expires',
            'interval'
        ]

    def create(self, validated_data):
        interval_data = validated_data.pop('interval')
        interval_serializer = IntervalScheduleCreateSerializer(
            data=interval_data)

        interval_serializer.is_valid(raise_exception=True)
        interval = interval_serializer.save()
        periodic_task = PeriodicTask.objects.create(
            **validated_data,
            interval=interval,
            task=TICKET_SCRAPER_TASK
        )

        return periodic_task


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

    def validate_url(self, value):
        validate_if_url_allowed(ALEBILET_URL, value)
        return value

    def create(self, validated_data):
        periodic_task_data = validated_data.pop('periodic_task')
        periodic_task_serializer = PeriodicTaskCreateSerializer(
            data=periodic_task_data)

        periodic_task_serializer.is_valid(raise_exception=True)
        periodic_task = periodic_task_serializer.save()
        ticket_search = TicketSearch.objects.create(
            **validated_data, periodic_task=periodic_task)

        return ticket_search


class TicketSearchReadSerializer(serializers.ModelSerializer):
    periodic_task = PeriodicTaskReadSerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

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

    def get_created_at(self, instance):
        return get_formatted_date(instance.created_at)

    def get_updated_at(self, instance):
        return get_formatted_date(instance.updated_at)
