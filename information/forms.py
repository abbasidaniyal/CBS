from django import forms
from .models import ContactUs


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name','email','contact_number','query']
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
