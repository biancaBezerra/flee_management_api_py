from django.db.models import Q

class TaxiUtils:
    def __init__(self, request):
        self.request = request

    def filter_taxis(self, taxis, filter_by):
        # Implementação para filtrar táxis
        if filter_by is not None:
            # Check if it's a number (ID) or plate
            if filter_by.isdigit():  # If it's a number, assume it's the ID
                return taxis.filter(id=int(filter_by))
            else:  # If it's not a number, assume it's the plate
                return taxis.filter(plate__icontains=filter_by)
        return taxis

    def sort_taxis(self, taxis, sort_by):
        # Implementação para ordenar táxis
        if sort_by is not None:
            return taxis.order_by('-' + sort_by[1:] if sort_by.startswith('-') else sort_by)
        return taxis

    def search_taxis(self, taxis, search):
        # Implementação para pesquisar táxis
        if search is not None:
            return taxis.filter(Q(id__icontains=search) | Q(plate__icontains=search))
        return taxis

    def get_page_size(self):
        # Implementação para obter o tamanho da página
        page_size = self.request.query_params.get('page_size', 10)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 10
        return page_size

    def get_page_number(self):
        # Implementação para obter o número da página
        page_number = self.request.query_params.get('page', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1
        return page_number
    
class TrajectoriesUtils:
    def __init__(self, request):
        self.request = request
    
    def filter_trajectories(self, trajectories, filter_by):
      # Implementação para filtrar táxis
      if filter_by is not None:
          # Check if it's a number (ID) or plate
          if filter_by.isdigit():  # If it's a number, assume it's the ID
              return trajectories.filter(taxi__id=int(filter_by))
          else:  # If it's not a number, assume it's the plate
              return trajectories.filter(taxi__plate__icontains=filter_by)
      return trajectories
    
    def sort_trajectories(self, trajectories, sort_by):
        # Ordenar trajetórias por data, id, latitude e longitude
      if sort_by is not None:
        return trajectories.order_by('-' + sort_by[1:] if sort_by.startswith('-') else sort_by)
      return trajectories
    
    def search_trajectories(self, trajectories, search):
        # Implementação para pesquisar táxis
        if search is not None:
            return trajectories.filter(Q(taxi__id__icontains=search) | Q(taxi__plate__icontains=search))
        return trajectories
    
    def get_page_size(self):
        # Implementação para obter o tamanho da página
        page_size = self.request.query_params.get('page_size', 10)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 10
        return page_size

    def get_page_number(self):
        # Implementação para obter o número da página
        page_number = self.request.query_params.get('page', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1
        return page_number
