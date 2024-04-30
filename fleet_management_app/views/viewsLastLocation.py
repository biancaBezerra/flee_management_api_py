# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from ..utils import LastLocationsUtils
from ..serializers import  TrajectoriesSerializer
from ..schemas import last_location_schema


@api_view(['GET'])
def get_last_location(request):
    if request.method == 'GET':
        # Instanciar a classe LastLocationsUtils com o objeto de request
        last_locations_utils = LastLocationsUtils(request)

        # Obter parâmetros de consulta da solicitação
        filter_by = request.query_params.get('filter_by')
        sort_by = request.query_params.get('sort_by')
        search = request.query_params.get('search')
        
        # Get page size and page number
        page_size = last_locations_utils.get_page_size()
        page_number = last_locations_utils.get_page_number()

         # Get the latest locations of all taxis
        last_trajectories = last_locations_utils.get_last_taxi_locations()

        # Check if the list of taxis is empty
        if not last_trajectories:
            return Response({'detail': 'Nenhum táxi encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Filter, sort and search trajectories
        last_trajectories = last_locations_utils.filter_last_locations(last_trajectories, filter_by)
        last_trajectories = last_locations_utils.search_last_locations(last_trajectories, search)
        last_trajectories = last_locations_utils.sort_last_locations(last_trajectories, sort_by)

        # Paginate the queryset using PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(last_trajectories, request)

        # Verificar se a lista de táxis está vazia
        if not result_page:
            return Response({'detail': 'Nenhuma localização encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
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

# Esquema personalizado para documentar a visualização de última localização do táxi no Swagger
get_last_location = last_location_schema(method='get')(get_last_location)


# def databaseEmDjango():
#     data = User.objects.get(pk='gabriel_nick')          # OBJETO
#     data = User.objects.filter(user_age='25')           # QUERYSET
#     data = User.objects.exclude(user_age='25')          # QUERYSET
#     data.save()
#     data.delete()