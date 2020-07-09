from django import forms
from .models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ["name", "email", "organisation", "contact_number", "query"]
        verbose_name = "Query"
        verbose_name_plural = "Queries"

        widgets = {
            "query": forms.Textarea(attrs={"rows": 4, "cols": 15}),
        }
