from django.urls import path
from .views import ComputeValueAPIView

urlpatterns = [
    path('ingester/', ComputeValueAPIView.as_view(), name='message-ingester'),
]
