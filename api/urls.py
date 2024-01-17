from django.urls import path, include

urlpatterns = [
    path('conv/', include('photo_conversion.urls')),
    path('acc/', include('account.urls')),
]
