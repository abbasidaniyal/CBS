from django import forms


class BulkImportForm(forms.Form):
    """Form for uploading zip file for bulk import"""
    zip_file = forms.FileField(
        label='Upload Zip File',
        help_text='Upload a zip file containing CSV files (clients.csv, projects.csv, gallery_images.csv) and image folders',
        widget=forms.FileInput(attrs={'accept': '.zip'})
    )
