# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Guide, GuideVersion, GuideElement
from .serializers import GuideSerializer, GuideElementsSerializer
from django.utils.dateparse import parse_date
from datetime import date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.


@swagger_auto_schema(
    method='get',
    operation_description="Получение справочников",
    responses={
        200: GuideSerializer(many=True),
        400: "Неправильная дата",
    },
    manual_parameters=[
        openapi.Parameter(
            'date',
            openapi.IN_QUERY,
            description="Дата начала действия в формате ГГГГ-ММ-ДД. Если указана, то \
                должны возвратиться только те справочники, в которых имеются \
                Версии с Датой начала действия раннее или равной указанной.",
            type=openapi.TYPE_STRING
        ),
    ]
)
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


@swagger_auto_schema(
    method='get',
    operation_description="Получение элементов справочника",
    responses={
        200: GuideElementsSerializer(many=True),
        400: "Неправильная версия",
    },
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_QUERY,
            description="Идентификатор справочника",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'version',
            openapi.IN_QUERY,
            description="Версия справочника. Если не указана, \
            то должны возвращаются элементы текущей версии. Текущей является та версия, \
            дата начала действия которой позже всех остальных версий данного справочника, \
            но не позже текущей даты.",
            type=openapi.TYPE_STRING
        ),

    ]
)
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


@swagger_auto_schema(
    method='get',
    operation_description="Проверка элемента справочника",
    responses={
        200: openapi.Response(
            description='Успешный ответ',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'valid': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Имеется ли такой элемент в справочнике")},
            )
        ),
        400: "Требуется код и значение справочника",
        404: "Неверно указан код или значение справочника или такого справочника не существует",
    },
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_QUERY,
            description="Идентификатор справочника",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'code',
            openapi.IN_QUERY,
            description="Код элемента справочника",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'value',
            openapi.IN_QUERY,
            description="Значение элемента справочника",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'version',
            openapi.IN_QUERY,
            description="Версия справочника.\
            Если не указана, то должны проверяться элементы в текущей версии.\
            Текущей является та версия, дата начала действия которой позже всех остальных\
            версий данного справочника, но не позже текущей даты.",
            type=openapi.TYPE_STRING
        ),
    ]
)
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
