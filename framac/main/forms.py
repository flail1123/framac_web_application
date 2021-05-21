from django import forms
from django.core.exceptions import ValidationError

def validateFile(value):
    if not value.name.endswith(".c"): 
        raise ValidationError('Unsupported file extension.')

class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validateFile])
    