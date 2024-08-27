# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Guide, GuideVersion, GuideElement
from django.utils.dateparse import parse_date


class GuideElementTests(APITestCase):
    def setUp(self):
        self.guide = Guide.objects.create(name="Test Guide")
        self.guide_version = GuideVersion.objects.create(
            idGuide=self.guide,
            version="1.0",
            dateStart=parse_date("2024-01-01")
        )
        self.guide_element = GuideElement.objects.create(
            idVersion=self.guide_version,
            elementCode="test_code",
            elementValue="test_value"
        )

    def test_check_element_exists(self):
        response = self.client.get('/refbooks/{}/check_element/'.format(
            self.guide.id), {'code': 'test_code', 'value': 'test_value'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"valid": True})

    def test_check_element_does_not_exist(self):
        response = self.client.get('/refbooks/{}/check_element/'.format(
            self.guide.id), {'code': 'nonexistent_code', 'value': 'test_value'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"valid": False})
