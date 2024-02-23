from django.urls import path
from .views import ConversionInitiationView, ConversionDetailView, ConversionListView, ConversionCheckView

# appends to /api/comv/
urlpatterns = [
    path('check/', ConversionCheckView.as_view(), name='check-conversion'),
    path('initiate/', ConversionInitiationView.as_view(), name='initiate-conversion'),
    path('<str:reference_id>/', ConversionDetailView.as_view(), name='conversion-detail'),
    path('', ConversionListView.as_view(), name='conversion-list'),
]