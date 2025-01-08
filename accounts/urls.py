from django.urls import path
from .views import RegisterView, CustomLoginView, TemplateView
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('home/', TemplateView.as_view(template_name='accounts/home.html'), name='home'),
]
