from django.contrib.auth.views import LoginView
from django.urls import reverse


class LandingLoginView(LoginView):
    """Always send users to the content landing page after login (ignore `?next=`)."""

    template_name = "registration/login.html"

    def get_success_url(self):
        return reverse("contentLanding")
