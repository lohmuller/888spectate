from datetime import timezone
import datetime
from model_bakery import baker
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
from ..queries.sports_queries import SportsQueries
from django.http import QueryDict
from ..models import Sport, Event, Selection
from ..queries.events_queries import EventsQueries


class EventsQueriesTestCase(TestCase):

    def setUp(self):
        # Criar objetos de teste necessários
        self.sport = Sport.objects.create(name="Test Sport", active=True)
        self.event = Event.objects.create(
            name="Test Event", sport=self.sport, active=True, scheduled_start='2023-10-30T12:00:00Z')

    def test_find_event(self):
        found_event = EventsQueries.find(self.event.id)
        self.assertEqual(found_event.id, self.event.id)

    def test_list_events_no_params(self):
        params = {}
        events = EventsQueries.list(params)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].id, self.event.id)

    def test_list_events_no(self):
        params = {
            "name": "Test Event",
        }
        events = EventsQueries.list(params)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].id, self.event.id)

    def test_list_events(self):
        params = {
            "name": "Test Event",
        }
        events = EventsQueries.list(params)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].id, self.event.id)

    def test_create_event(self):
        event_data = {
            "name": "New Event",
            "sport": int(self.sport.id),
            "status": "active",
            'slug': 'mock-event',
            'active': True,
            'type': 'preplay',
            'status': 'Pending',
            'scheduled_start': '2023-10-30T12:00:00Z',
            'actual_start': '2023-10-30T12:00:00Z'
        }
        new_event_id = EventsQueries.create(event_data)
        new_event = Event.objects.get(id=new_event_id)
        self.assertEqual(new_event.name, "New Event")
