from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, LogoutView, ActivateUserView, CheckEmailTemplateView
# PasswordChangeView, PasswordResetView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('activate/<str:username>/<str:otp>/', ActivateUserView.as_view(), name='activate'),
    path('checkemailtemplate/', CheckEmailTemplateView.as_view(), name='checkemailtemplate'),
    # path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    # path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
]