from django.contrib.auth.views import LoginView
from django.urls import path

from accounts.views import logout_view, profile_view

urlpatterns = [
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login_page'),
    path('logout/', logout_view, name='logout_page'),
    path('profile/', profile_view, name='profile_page'),
]
