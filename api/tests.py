# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Guide, GuideVersion, GuideElement
from django.utils.dateparse import parse_date


class GuideModelTest(APITestCase):
    def setUp(self):
        self.guide = Guide.objects.create(
            code='Test50',
            name='Testname',
            description='Testdescription.'
        )

    def test_guide_exists(self):
        response = self.client.get('/refbooks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "refbooks": [
                {
                    "id": 1,
                    "code": "Test50",
                    "name": "Testname"
                }
            ]
        })


class GuideModelWithDateTest(APITestCase):
    def setUp(self):
        self.guide = Guide.objects.create(
            code='Test52',
            name='Testname2',
            description='Testdescription2.'
        )
        self.guide_version = GuideVersion.objects.create(
            idGuide=self.guide,
            version="20",
            dateStart=parse_date("2024-08-08")
        )

    def test_guide_exists(self):
        response = self.client.get('/refbooks/', {'date': '2024-08-08'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "refbooks": [
                {
                    "id": 1,
                    "code": "Test52",
                    "name": "Testname2"
                }
            ]
        })

    def test_guide_not_exists(self):
        response = self.client.get('/refbooks/', {'date': '2024-07-07'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "refbooks": []
        })


class GuideElementsTest(APITestCase):
    def setUp(self):
        self.guide = Guide.objects.create(
            code='Test52',
            name='Testname2',
            description='Testdescription2.'
        )
        self.guide_version = GuideVersion.objects.create(
            idGuide=self.guide,
            version="20",
            dateStart=parse_date("2024-08-08")
        )
        self.guide_element = GuideElement.objects.create(
            idVersion=self.guide_version,
            elementCode="TestCode",
            elementValue="TestValue"
        )

    def test_guide_exists(self):
        response = self.client.get(
            '/refbooks/{}/elements/'.format(self.guide.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'elements': [
                {
                    'elementCode': 'TestCode',
                    'elementValue': 'TestValue'
                }
            ]
        })

    def test_guide_with_version_exists(self):
        response = self.client.get(
            '/refbooks/{}/elements/'.format(self.guide.id), {'version': '20'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'elements': [
                {
                    'elementCode': 'TestCode',
                    'elementValue': 'TestValue'
                }
            ]
        })

    def test_guide_not_exists(self):
        response = self.client.get(
            '/refbooks/{}/elements/'.format(self.guide.id), {'version': '19'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GuideCheckElementTests(APITestCase):
    def setUp(self):
        self.guide = Guide.objects.create(code="T1", name="Test Guide")
        self.guide_version = GuideVersion.objects.create(
            idGuide=self.guide,
            version="1.0",
            dateStart=parse_date("2024-01-01")
        )
        self.guide_element = GuideElement.objects.create(
            idVersion=self.guide_version,
            elementCode="TestCode",
            elementValue="TestValue"
        )

    def test_check_element_exists(self):
        response = self.client.get('/refbooks/{}/check_element/'.format(
            self.guide.id), {'code': 'TestCode', 'value': 'TestValue'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"valid": True})

    def test_check_element_with_version_exists(self):
        response = self.client.get('/refbooks/{}/check_element/'.format(
            self.guide.id), {'code': 'TestCode', 'value': 'TestValue', 'version': '1.0'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"valid": True})

    def test_check_element_does_not_exist(self):
        response = self.client.get('/refbooks/{}/check_element/'.format(
            self.guide.id), {'code': 'nonexistent_code', 'value': 'TestValue'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"valid": False})
