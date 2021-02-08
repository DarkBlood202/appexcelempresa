from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class FechaForm(forms.Form):
    fecha_inicio = forms.DateField()
    fecha_fin = forms.DateField()