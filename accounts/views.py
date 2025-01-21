from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserForm, ProfileForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Profile


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


class UserInformationView(LoginRequiredMixin, TemplateView):
    template_name = "user_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = CustomUserCreationForm(instance=self.request.user)
        profile_form = ProfileForm(instance=self.request.user.profile)
        context["user_form"] = user_form
        context["profile_form"] = profile_form
        return context

    def post(self, request, *args, **kwargs):
        user_form = CustomUserCreationForm(request.POST, instance=self.request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(self.request, f"Account created successfully")
            redirect('checkout')

        else:
            messages.error(self.request, "Please correct the error below.")
            return self.render_to_response(self.get_context_data())


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['address', 'phone_number']
    template_name = 'accounts/edit_profile.html'

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        messages.success(self.request, "Profile updated successfully")
