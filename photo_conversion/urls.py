from django.urls import path
from .views import ConversionInitiationView, ConversionDetailView, ConversionListView

urlpatterns = [
    path('initiate/', ConversionInitiationView.as_view(), name='initiate-conversion'),
    path('<str:reference_id>/', ConversionDetailView.as_view(), name='conversion-detail'),
    path('', ConversionListView.as_view(), name='conversion-list'),
]