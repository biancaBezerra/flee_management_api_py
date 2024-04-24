from django.db.models import Q

class BaseUtils:
    def __init__(self, request):
        self.request = request
    
    def filter_objects(self, queryset, filter_by, id_field, plate_field):
        if filter_by is not None:
            if filter_by.isdigit():
                return queryset.filter(**{id_field: int(filter_by)})
            else:
                return queryset.filter(**{plate_field + '__icontains': filter_by})
        return queryset
    
    def sort_objects(self, queryset, sort_by):
        if sort_by is not None:
            return queryset.order_by('-' + sort_by[1:] if sort_by.startswith('-') else sort_by)
        return queryset
    
    def search_objects(self, queryset, search, id_field, plate_field):
        if search is not None:
            return queryset.filter(Q(**{id_field + '__icontains': search}) | Q(**{plate_field + '__icontains': search}))
        return queryset
    
    def get_page_size(self):
        page_size = self.request.query_params.get('page_size', 10)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 10
        return page_size
    
    def get_page_number(self):
        page_number = self.request.query_params.get('page', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1
        return page_number

class TaxiUtils(BaseUtils):
    def filter_taxis(self, taxis, filter_by):
        return self.filter_objects(taxis, filter_by, 'id', 'plate')
    
    def sort_taxis(self, taxis, sort_by):
        return self.sort_objects(taxis, sort_by)
    
    def search_taxis(self, taxis, search):
        return self.search_objects(taxis, search, 'id', 'plate')

class TrajectoriesUtils(BaseUtils):
    def filter_trajectories(self, trajectories, filter_by):
        return self.filter_objects(trajectories, filter_by, 'taxi__id', 'taxi__plate')
    
    def sort_trajectories(self, trajectories, sort_by):
        return self.sort_objects(trajectories, sort_by)
    
    def search_trajectories(self, trajectories, search):
        return self.search_objects(trajectories, search, 'taxi__id', 'taxi__plate')
