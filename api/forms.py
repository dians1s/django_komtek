from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Guide, GuideVersion, GuideElement


class GuideVersionForm(forms.ModelForm):
    class Meta:
        model = GuideVersion
        fields = ['codeGuide', 'version', 'dateStart']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codeGuide'].queryset = Guide.objects.all()
        self.fields['codeGuide'].label_from_instance = lambda obj: f"{
            obj.code} - {obj.name}"


class GuideElementForm(forms.ModelForm):
    class Meta:
        model = GuideElement
        fields = ('idVersion', 'elementCode', 'elementValue')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idVersion'].queryset = GuideVersion.objects.all()
        self.fields['idVersion'].label_from_instance = lambda obj: f"{
            obj.codeGuide.code} - {obj.codeGuide.name} | {obj.version}"
