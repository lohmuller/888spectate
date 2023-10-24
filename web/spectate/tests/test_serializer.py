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

# @TODO
