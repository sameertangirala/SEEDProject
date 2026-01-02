from django.urls import path
from .views import AppLinkList

urlpatterns = [
    path('apps/', AppLinkList.as_view(), name='app-list'),
]
