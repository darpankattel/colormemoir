from django.urls import path, include

# appends with /api/

urlpatterns = [
    path('conv/', include('photo_conversion.urls')),
    path('acc/', include('account.urls')),
]
