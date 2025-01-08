from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from ..forms import ClientRegistrationForm

class ClientRegistrationView(CreateView):
    template_name = "clients/register.html"
    form_class = ClientRegistrationForm
    success_url = reverse_lazy("client_home")
