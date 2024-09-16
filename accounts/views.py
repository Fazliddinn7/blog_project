from django.contrib.auth import logout
from django.shortcuts import render


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


def profile_view(request):
    user = request.user
    return render(request, 'pages/user_profile.html', {'user':user})
