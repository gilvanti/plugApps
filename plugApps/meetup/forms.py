#pylint: disable=E1101
from django import forms
from meetup.models import (Meeting)
from django.forms.widgets import ClearableFileInput

class MeetingCreateForm(forms.ModelForm):
    """Formulário para criação de reuniões"""

    imagem = forms.ImageField(widget=ClearableFileInput)
    data_hora = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Meeting
        exclude = ["user"]

    def clean_foto(self):
        """Valida formato do arquivo anexado"""
        imagem = self.cleaned_data.get("foto")
        permited_extensions = ["png", "jpg", "jpeg"]
        if imagem:
            if not foto.name.split(".")[-1] in permited_extensions:
                self.add_error("imagem", "Formato inválido. A foto deve ser png, jpg ou jpeg.")
        return imagem

class MeetingEditForm(forms.ModelForm):
    """Formulário para edição de reuniões"""

    imagem = forms.ImageField(widget=ClearableFileInput)
    data_hora = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Meeting
        exclude = ["user"]

    def clean_foto(self):
        """Valida formato do arquivo anexado"""
        imagem = self.cleaned_data.get("foto")
        permited_extensions = ["png", "jpg", "jpeg"]
        if imagem:
            if not foto.name.split(".")[-1] in permited_extensions:
                self.add_error("imagem", "Formato inválido. A foto deve ser png, jpg ou jpeg.")
        return imagem
