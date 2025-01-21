from django.urls import path
from .views import RegisterView, CustomLoginView, TemplateView, ProfileEditView
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', ProfileEditView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('home/', TemplateView.as_view(template_name='accounts/home.html'), name='home'),
]
