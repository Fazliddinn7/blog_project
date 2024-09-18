from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from accounts.forms import UserRegistrationForm


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


def profile_view(request):
    user = request.user
    return render(request, 'pages/user_profile.html', {'user': user})


# class SignUpView(View):
#
#     def get(self, request):
#         user_form = UserRegistrationForm()
#         return render(request, 'account/register.html', {'user_form': user_form})
#
#     def post(self, request):
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(
#                 user_form.cleaned_data['password']
#             )
#             new_user.save()
#         return render(request, 'account/register_done.html', {'user_form': user_form})


class SignUpView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login_page')
    template_name = 'account/register.html'
