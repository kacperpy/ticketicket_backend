from django.db import router
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ticket.api import views


router = DefaultRouter()
router.register(r"ticket-searches", views.TicketSearchViewSet,
                basename='ticket-searches')

urlpatterns = [
    path('', include(router.urls)),
]
