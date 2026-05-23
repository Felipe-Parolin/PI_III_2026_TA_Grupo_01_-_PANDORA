from django.urls import path
from app_core.views import OnboardingView

urlpatterns = [
    path('owner/onboarding/', OnboardingView.as_view(), name='onboarding'),
]