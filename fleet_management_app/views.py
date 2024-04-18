# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


from .models import Taxis, Trajectories
from .serializers import TaxisSerializer, TrajectoriesSerializer
from .schemas import taxis_list_schema, trajectories_list_schema


@api_view(['GET'])
def get_taxis(request):
    if request.method == 'GET':
        taxis = Taxis.objects.all()                      # Get all objects in Tax's database (It returns a queryset)

        # Aplicar filtro pelo ID ou pela placa
        filter_by = request.query_params.get('filter_by', None)
        if filter_by:
            try:
                filter_by_id = int(filter_by)
                taxis = taxis.filter(id=filter_by_id)
            except ValueError:
                taxis = taxis.filter(plate__icontains=filter_by)

        # Lógica para aplicar ordenação
        sort_by = request.query_params.get('sort_by', None)
        if sort_by:
            if sort_by.startswith('-'):
                # Ordenação descendente
                sort_by_field = sort_by[1:]
                taxis = taxis.order_by('-' + sort_by_field)
            else:
                # Ordenação ascendente
                taxis = taxis.order_by(sort_by)

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
get_taxis = taxis_list_schema(method='get')(get_taxis) #um schema personalizado para documentar a visualização de taxis nos swagger


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
get_trajectories = trajectories_list_schema(method='get')(get_trajectories)

# def databaseEmDjango():
#     data = User.objects.get(pk='gabriel_nick')          # OBJETO
#     data = User.objects.filter(user_age='25')           # QUERYSET
#     data = User.objects.exclude(user_age='25')          # QUERYSET
#     data.save()
#     data.delete()