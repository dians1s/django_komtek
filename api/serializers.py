from rest_framework import serializers
from .models import Guide, GuideElement


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('id', 'code', 'name')


class GuideElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideElement
        fields = ('elementCode', 'elementValue')
