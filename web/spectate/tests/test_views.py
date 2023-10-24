from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
from django.http import QueryDict
from ..models import Sport, Event, Selection
from datetime import datetime, timezone


class SportsViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.sport_data = {'name': 'Futebol',
                           'slug': 'slug-example', 'active': True}

    @patch('spectate.queries.sports_queries.SportsQueries.list')
    def test_list_sports_with_mock(self, mock_sports_queries_list):
        expected_data = [self.sport_data]
        query_params = QueryDict(query_string='name=Futebol')

        mock_sports_queries_list.return_value = expected_data

        url = reverse('sports-list')
        response = self.client.get(url, query_params)

        mock_sports_queries_list.assert_called_once_with(query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    @patch('spectate.queries.sports_queries.SportsQueries.create')
    def test_create_sport_with_mock(self, mock_create):
        sport_data = self.sport_data
        creation_id = 1

        mock_create.return_value = creation_id

        url = reverse('sports-list')
        response = self.client.post(url, data=sport_data, format='json')

        mock_create.assert_called_once_with(sport_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': creation_id, **sport_data})

    @patch('spectate.queries.sports_queries.SportsQueries.find')
    @patch('spectate.queries.sports_queries.SportsQueries.update')
    def test_update_sport_with_mock(self, mock_update, mock_find):
        sport_data = self.sport_data
        id = 3

        mock_update.return_value = True
        mock_find.return_value = Sport(id=3, **sport_data)

        url = reverse('sports-detail', args=[id])
        response = self.client.patch(url, data=sport_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_update.assert_called_once_with(id, sport_data)
        self.assertEqual(response.data, sport_data)


class EventsViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.event_data = {
            'name': 'Mock Event',
            'slug': 'mock-event',
            'active': True,
            'type': 'preplay',
            'sport': 1,
            'status': 'Pending',
            'scheduled_start': datetime.strptime('2023-10-30T12:00:00Z', '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc),
            'actual_start': datetime.strptime('2023-10-30T12:00:00Z', '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)}
        self.request_data = {
            'name': 'Mock Event',
            'slug': 'mock-event',
            'active': True,
            'type': 'preplay',
            'sport': 1,
            'status': 'Pending',
            'scheduled_start': '2023-10-30T12:00:00Z',
            'actual_start': '2023-10-30T12:00:00Z', }

    @patch('spectate.queries.events_queries.EventsQueries.list')
    def test_list_events_with_mock(self, mock_events_queries_list):
        data = self.event_data
        data['sport'] = Sport(id=1)
        expected_data = [data]
        query_params = QueryDict(query_string='name=Futebol')

        mock_events_queries_list.return_value = expected_data

        url = reverse('events-list')
        response = self.client.get(url, query_params)

        self.assertEqual(response.data[0]['name'], expected_data[0]['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_events_queries_list.assert_called_once_with(query_params)

    @patch('spectate.queries.sports_queries.SportsQueries.find')
    @patch('spectate.queries.events_queries.EventsQueries.create')
    def test_create_event_with_mock(self, mock_create, mock_sport_find):
        event_data = self.event_data
        creation_id = 1

        mock_create.return_value = creation_id
        mock_sport_find.return_value = Sport(id=1)

        url = reverse('events-list')
        response = self.client.post(url, data=event_data, format='json')

        self.assertEqual(response.data, {'id': creation_id, **event_data})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_create.assert_called_once_with(event_data)

    @patch('spectate.queries.sports_queries.SportsQueries.find')
    @patch('spectate.queries.events_queries.EventsQueries.find')
    @patch('spectate.queries.events_queries.EventsQueries.update')
    def test_update_event_with_mock(self, mock_update, mock_find, mock_sport_find):
        event_data = self.event_data
        event_data['sport'] = Sport(id=1)
        id = 3

        mock_sport_find.return_value = Sport(id=1)
        mock_update.return_value = True
        mock_find.return_value = Event(id=id, **event_data)

        url = reverse('events-detail', args=[id])
        response = self.client.patch(
            url, data=self.request_data, format='json')

        self.assertEqual(response.data, {**event_data, 'sport': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_update.assert_called_once_with(id, {**event_data, 'sport': 1})
