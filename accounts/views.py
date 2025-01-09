from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy


# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Account created successfully for {form.cleaned_data["username"]}')
#             return redirect('login')
#         else:
#             messages.error(request, 'Registration failed. Please check the form.')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'accounts/register.html', {"form": form})
#
#
# def login_view(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('login')
#         else:
#             form = CustomAuthenticationForm()
#         return render(request, 'accounts/login.html', {"form": form})


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f"Account created successfully for {form.cleaned_data['username']}")
        print(" Form is valid. Redirecting to login page")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please check the form.")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm

    # def form_valid(self, form):
    #     user = form.get_user()
    #     login(self.request, user)
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_list')


# class HomeView(TemplateView):
#     template_name = 'accounts/home.html'
