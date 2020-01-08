from django.urls import re_path
from .consumers import WorkConsumer

websocket_urlpatterns = [
    re_path(r'ws/companies/$', WorkConsumer),
]
