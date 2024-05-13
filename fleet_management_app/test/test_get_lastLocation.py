import pytest
from rest_framework.test import APIRequestFactory
from fleet_management_app.views.viewsLastLocation import get_last_location
from fleet_management_app.models import Trajectories, Taxis
from unittest.mock import patch
from datetime import datetime

@pytest.fixture(scope='module')
def mock_trajectories_queryset(request):
    mock_taxis_trajectories = [
        Taxis(id=1991, plate="JAY-3232"),
        Taxis(id=1995, plate="BIA-4545"),
    ]

    mock_trajectories = [
        Trajectories(id=1991, taxi=mock_taxis_trajectories[0], date=datetime(2023, 12, 25, 1, 10, 2), latitude=22.1234, longitude=22.9012),
        Trajectories(id=1995, taxi=mock_taxis_trajectories[1], date=datetime(2023, 11, 21, 1,10,3), latitude=12.9876, longitude=25.8765),
        Trajectories(id=1991, taxi=mock_taxis_trajectories[0], date=datetime(2023, 12, 24, 1, 10, 2), latitude=22.5678, longitude=22.3456),
        Trajectories(id=1995, taxi=mock_taxis_trajectories[1], date=datetime(2023, 11, 20, 1,10,3), latitude=12.5432, longitude=25.8765),
        Trajectories(id=1991, taxi=mock_taxis_trajectories[0], date=datetime(2023, 12, 23, 1, 10, 2), latitude=22.9012, longitude=22.7890),
        Trajectories(id=1995, taxi=mock_taxis_trajectories[1], date=datetime(2023, 11, 19, 1,10,3), latitude=12.1098, longitude=25.8765)
    ]

    with patch('fleet_management_app.views.viewsLastLocation.LastLocationsUtils.get_last_taxi_locations') as mock_trajectories_queryset:
        mock_trajectories_queryset.return_value = mock_trajectories
        yield mock_trajectories_queryset

def test_list_lastlocation_endpoint(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint
    request = factory.get('/api/lastlocation/')
    response = get_last_location(request)

    # Asserting that the list of taxis is not empty
    assert response.status_code == 200
    assert len(response.data['results']) > 0


    # Getting the latest trajectory from the results
    assert response.data['results'][0]['date'] == '2023-12-25T01:10:02Z'
    assert response.data['results'][1]['date'] == '2023-11-21T01:10:03Z'


# def test_list_lastlocation_filter(mock_trajectories_queryset):
#     factory = APIRequestFactory()

#     # Making a GET request to the endpoint with filter parameter
#     request = factory.get('/api/lastlocation/', {'taxi__plate': 'JAY-3232'})
#     response = get_last_location(request)

#     # Asserting the response data
#     assert response.status_code == 200
#     assert len(response.data['results']) == 6
#     assert response.data['results'][0]['taxi']['plate'] == 'JAY-3232'

# def test_list_trajectories_sort(mock_trajectories_queryset):
#     factory = APIRequestFactory()

#     # Making a GET request to the endpoint with sort parameter
#     request = factory.get('/api/trajectories/', {'order_by': '-taxi__plate'})
#     response = get_last_location(request)

#     # Asserting the response data
#     assert response.status_code == 200
#     assert len(response.data['results']) == 4
#     assert response.data['results'][3]['taxi']['plate'] == 'BIA-4545'
#     assert response.data['results'][1]['taxi']['plate'] == 'CNCJ-4562'
#     assert response.data['results'][0]['taxi']['plate'] == 'PGF-7794'
#     assert response.data['results'][2]['taxi']['plate'] == 'JAY-3232'

# def test_list_trajetories_search(mock_trajectories_queryset):
#     factory = APIRequestFactory()

#     # Making a GET request to the endpoint with search parameter
#     request = factory.get('/api/trajectories/', {'taxi__id': 1991})
#     response = get_last_location(request)

#     # Asserting the response status code
#     assert response.status_code == 200

#     # Asserting the response data
#     assert len(response.data['results']) == 4
#     assert response.data['results'][2]['taxi']['id'] == 1991

# def test_list_trajectories_pagination(mock_trajectories_queryset):
#     mock_taxis_trajectories = [Taxis(id=i, plate=f"ABC-{i}") for i in range(1, 21)]  # foram criados 20 taxis mock
#     mock_trajectories = [
#         Trajectories(
#             id=i, 
#             taxi=mock_taxis_trajectories[i - 1], 
#             date=datetime(i,m,i,i,i,i), 
#             latitude=i, 
#             longitude=i
#             ) 
#             for i in range(1, 21) for m in range(1,12)
#     ]
    
#     mock_trajectories_queryset.return_value = mock_trajectories

#     factory = APIRequestFactory()

#     request = factory.get('/api/trajectories/', {'page': 1})
#     response = get_last_location(request)

#     # Asserting the response status code
#     assert response.status_code == 200

#     # Asserting the response data
#     assert len(response.data['results']) == 10  # Aqui assumimos que será retornado 10 taxis por pagina
#     assert response.data['current_page'] == 1
#     assert response.data['total_pages'] == 22
#     assert response.data['next'] is not None
#     assert response.data['previous'] is None