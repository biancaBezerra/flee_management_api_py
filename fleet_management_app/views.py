# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Taxis, Trajectories
from .serializers import TaxisSerializer, TrajectoriesSerializer

import json

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Número da página'),
        openapi.Parameter('page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Tamanho da página'),
        openapi.Parameter('sort_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Ordenar por campo'),
        openapi.Parameter('filter_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Filtrar por campo'),
        openapi.Parameter('search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Termo de busca'),
    ],
    responses={200: openapi.Response(
        'List of taxis',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'current_page': openapi.Schema(type=openapi.TYPE_INTEGER),
                'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER),
                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                'next': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'previous': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'results': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'plate': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    )
                ),
            }
        )
    ),
     400: "Bad request",
     404: "Not found",
    },
    operation_summary="Get Taxis",
    operation_description="Get a list of all taxis."
)

@api_view(['GET'])
def get_taxis(request):
    if request.method == 'GET':
        taxis = Taxis.objects.all()                          # Get all objects in Tax's database (It returns a queryset)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(taxis, request)
        serializer = TaxisSerializer(result_page, many=True)       # Serialize the object data into json (Has a 'many' parameter cause it's a queryset)
        response = paginator.get_paginated_response(serializer.data)
        # Including additional pagination information at the beginning of the response object
        pagination_info = {
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages
        }
        # Adding pagination information at the beginning of the response object
        response.data = {**pagination_info, **response.data}
        return response                   # Return the serialized data
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='page number'),
        openapi.Parameter('page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='page size'),
        openapi.Parameter('sort_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Sort by field'),
        openapi.Parameter('filter_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Filter by field'),
        openapi.Parameter('search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Search term'),
    ],
    responses={200: openapi.Response(
        'List of trajectories',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'current_page': openapi.Schema(type=openapi.TYPE_INTEGER),
                'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER),
                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                'next': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'previous': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'results': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'taxi': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'plate': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            ),
                            'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                            'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                            'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                        }
                    )
                ),
            }
        )
    ),
    400: "Bad request",
    404: "Not found",
    },
    operation_summary="Get Trajectories",
    operation_description="Get a list of all trajectories."
)
@api_view(['GET'])
def get_trajectories(request):
    if request.method == 'GET':
        trajectories = Trajectories.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10 #paginação dos dados
        result_page = paginator.paginate_queryset(trajectories, request)
        serializer = TrajectoriesSerializer(result_page, many=True)
        response = paginator.get_paginated_response(serializer.data)
        # Including additional pagination information at the beginning of the response object
        pagination_info = {
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages
        }
        # Adding pagination information at the beginning of the response object
        response.data = {**pagination_info, **response.data}
        return response   # Return the serialized data
    return Response(status=status.HTTP_400_BAD_REQUEST) 

# def databaseEmDjango():
#     data = User.objects.get(pk='gabriel_nick')          # OBJETO
#     data = User.objects.filter(user_age='25')           # QUERYSET
#     data = User.objects.exclude(user_age='25')          # QUERYSET
#     data.save()
#     data.delete()