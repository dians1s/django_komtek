# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Guide, GuideVersion, GuideElement
from .serializers import GuideSerializer, GuideElementsSerializer
from django.utils.dateparse import parse_date
from datetime import date

# Create your views here.


@api_view(['GET'])
def refbooks_list(request):
    date_str = request.GET.get('date', None)

    if date_str:
        try:
            date = parse_date(date_str)
            if not date:
                return Response({"error": "Invalid date"}, status=status.HTTP_400_BAD_REQUEST)
            guides = Guide.objects.filter(
                guideversion__dateStart__lte=date).distinct()
        except:
            return Response({"error": "Invalid date"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        guides = Guide.objects.all()

    serializer = GuideSerializer(guides, many=True)

    return Response({"refbooks": serializer.data})


@api_view(['GET'])
def guide_elements(request, id):

    version = request.GET.get('version', None)

    try:
        idGuide = Guide.objects.get(id=id)
    except:
        return Response({"error": "Guide not found"}, status=status.HTTP_404_NOT_FOUND)

    if version:
        try:
            idVersion = GuideVersion.objects.get(
                idGuide=idGuide, version=version)
        except:
            return Response({"error": "Guide version not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        idVersion = GuideVersion.objects.filter(
            idGuide=idGuide, dateStart__lte=date.today()).latest('dateStart')
        if not idVersion:
            return Response({"error": "No current version found"}, status=status.HTTP_404_NOT_FOUND)

    elements = GuideElement.objects.filter(idVersion=idVersion)
    serializer = GuideElementsSerializer(elements, many=True)

    return Response({"elements": serializer.data})


@api_view(['GET'])
def check_element(request, id):

    code = request.GET.get('code')
    value = request.GET.get('value')
    version = request.GET.get('version', None)

    if not code or not value:
        return Response({"error": "Required code and value params"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        idGuide = Guide.objects.get(id=id)
    except:
        return Response({"error": "Guide not found"}, status=status.HTTP_404_NOT_FOUND)

    if version:
        try:
            idVersion = GuideVersion.objects.get(
                idGuide=idGuide, version=version)
        except:
            return Response({"error": "Version not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        idVersion = GuideVersion.objects.filter(
            idGuide=idGuide, dateStart__lte=date.today()).latest('dateStart')
        if not idVersion:
            return Response({"error": "Version not found"}, status=status.HTTP_404_NOT_FOUND)

    res = GuideElement.objects.filter(
        idVersion=idVersion, elementCode=code, elementValue=value).exists()

    if res:
        return Response({"valid": True})
    else:
        return Response({"valid": False})
