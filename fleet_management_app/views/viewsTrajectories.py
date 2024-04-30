from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from ..utils import TrajectoriesUtils
from ..models import Trajectories
from ..serializers import TrajectoriesSerializer
from ..schemas import trajectories_list_schema

@api_view(['GET'])
def get_trajectories(request):
    if request.method == 'GET':
        # Instanciar a classe TaxiUtils com o objeto de request
        trajectories_utils = TrajectoriesUtils(request)

        # Get request query parameters
        filter_by = request.query_params.get('filter_by')
        sort_by = request.query_params.get('sort_by')
        search = request.query_params.get('search')

        # Get page size and page number usando os métodos da classe
        page_size = trajectories_utils.get_page_size()
        page_number = trajectories_utils.get_page_number()

        # Filter, sort, and search trajectories usando os métodos da classe
        trajectories = Trajectories.objects.all()
        trajectories = trajectories_utils.filter_trajectories(trajectories, filter_by)
        trajectories = trajectories_utils.sort_trajectories(trajectories, sort_by)
        trajectories = trajectories_utils.search_trajectories(trajectories, search) 

        # Paginate the queryset using PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(trajectories, request)               

        # Verificar se a lista de táxis está vazia
        if not result_page:
            return Response({'detail': 'Nenhum táxi encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
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
