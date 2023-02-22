from django.contrib import messages
from django.shortcuts import render, reverse
from django.views import generic
from .forms import ContactForm
from django.core.mail import send_mail
from cart.models import Product

from django.conf import settings

# Create your views here.

class HomeView(generic.TemplateView):
    template_name = 'index.html'

class ContactView(generic.FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def get_url(self):
        return reverse('contact')

    def form_valid(self, form):
        messages.info(self.request, 'Thanks for getting intouch')
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')

        full_message =f""" Received message from {name} {email}


        {message}
        """

        send_mail(
            subject='hello',
            message=full_message,
            from_email= settings.DEFAULT_FROM_EMAIL,
            recipient_list= [settings.NOTIFY_EMAIL]

        )

        return super(ContactView, self).form_valid(form)
