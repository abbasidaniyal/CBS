from django import forms
from .models import ContactUs


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email','organisation', 'contact_number', 'query']
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

        widgets = {
            'query': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }