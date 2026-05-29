from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import StaffSignUpForm


class LandingLoginView(LoginView):
    """Always send users to the content landing page after login (ignore `?next=`)."""

    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("contentLanding")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("contentLanding")


class SignUpView(CreateView):
    """Register a staff account, then sign in and go to content management."""

    form_class = StaffSignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("contentLanding")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("contentLanding")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(
            self.request,
            "Your account is ready. You can manage content, CRM, and account settings from here.",
        )
        return response
