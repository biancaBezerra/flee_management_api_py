import pytest
from rest_framework.test import APIRequestFactory
from fleet_management_app.views.viewsTrajectories import get_trajectories
from fleet_management_app.models import Trajectories, Taxis
from unittest.mock import patch
from datetime import datetime

@pytest.fixture(scope='module')
def mock_trajectories_queryset(request):
    mock_taxis_trajectories = [
        Taxis(id=10133, plate="PGF-7794"),
        Taxis(id=7249, plate="CNCJ-4562"),
        Taxis(id=1991, plate="JAY-3232"),
        Taxis(id=1995, plate="BIA-4545"),
    ]

    mock_trajectories = [
        Trajectories(id=10133, taxi=mock_taxis_trajectories[0], date=datetime(2024, 5, 10, 5, 10, 2), latitude=10.1234, longitude=20.5678),
        Trajectories(id=7249, taxi=mock_taxis_trajectories[1], date=datetime(2024, 5, 9, 9,10,3), latitude=11.4321, longitude=21.8765),
        Trajectories(id=1991, taxi=mock_taxis_trajectories[2], date=datetime(2023, 12, 25, 1, 10, 2), latitude=22.1234, longitude=22.5678),
        Trajectories(id=1995, taxi=mock_taxis_trajectories[3], date=datetime(2023, 11, 22, 1,10,3), latitude=12.4321, longitude=25.8765)
    ]
    with patch('fleet_management_app.views.viewsTrajectories.Trajectories.objects.all') as mock_trajectories_queryset:
        # Crie um mock do queryset de Trajectories
        mock_trajectories_queryset.return_value = mock_trajectories
        yield mock_trajectories_queryset

def test_list_trajectories_endpoint(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint
    request = factory.get('/api/trajectories/')
    response = get_trajectories(request)

    # Asserting that the list of taxis is not empty
    assert response.status_code == 200
    assert len(response.data['results']) > 0

def test_list_trajectories_filter(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with filter parameter
    request = factory.get('/api/trajectories/', {'taxi__plate': 'PGF-7794'})
    response = get_trajectories(request)

    # Asserting the response data
    assert response.status_code == 200
    assert len(response.data['results']) == 4
    assert response.data['results'][0]['taxi']['plate'] == 'PGF-7794'

def test_list_trajectories_sort(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with sort parameter
    request = factory.get('/api/trajectories/', {'order_by': '-taxi__plate'})
    response = get_trajectories(request)

    # Asserting the response data
    assert response.status_code == 200
    assert len(response.data['results']) == 4
    assert response.data['results'][3]['taxi']['plate'] == 'BIA-4545'
    assert response.data['results'][1]['taxi']['plate'] == 'CNCJ-4562'
    assert response.data['results'][0]['taxi']['plate'] == 'PGF-7794'
    assert response.data['results'][2]['taxi']['plate'] == 'JAY-3232'

def test_list_trajetories_search(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with search parameter
    request = factory.get('/api/trajectories/', {'taxi__id': 1991})
    response = get_trajectories(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 4
    assert response.data['results'][2]['taxi']['id'] == 1991

def test_list_trajectories_pagination(mock_trajectories_queryset):
    mock_taxis_trajectories = [Taxis(id=i, plate=f"ABC-{i}") for i in range(1, 21)]  # foram criados 20 taxis mock
    mock_trajectories = [
        Trajectories(
            id=i, 
            taxi=mock_taxis_trajectories[i - 1], 
            date=datetime(i,m,i,i,i,i), 
            latitude=i, 
            longitude=i
            ) 
            for i in range(1, 21) for m in range(1,12)
    ]
    
    mock_trajectories_queryset.return_value = mock_trajectories

    factory = APIRequestFactory()

    request = factory.get('http://localhost:8000/api/taxis/', {'page': 1})
    response = get_trajectories(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 10  # Aqui assumimos que será retornado 10 taxis por pagina
    assert response.data['current_page'] == 1
    assert response.data['total_pages'] == 22
    assert response.data['next'] is not None
    assert response.data['previous'] is None