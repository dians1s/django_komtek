from rest_framework import serializers
from .models import Guide, GuideElement


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('id', 'code', 'name')
        extra_kwargs = {
            'code': {'help_text': 'Код справочника'},
            'name': {'help_text': 'Название вашего справочника'},
        }


class GuideElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideElement
        fields = ('elementCode', 'elementValue')
        extra_kwargs = {
            'elementCode': {'help_text': 'Код элемента'},
            'elementValue': {'help_text': 'Значение элемента'},
        }
