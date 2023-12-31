from rest_framework import serializers
from .models import Sport, Event, Selection
from .queries.sports_queries import SportsQueries
from .queries.events_queries import EventsQueries
from django import forms

"""""
Not using Serializer to avoid ORM use while validating
"""""


class SportForm(forms.Form):
    name = forms.CharField(max_length=100)
    slug = forms.SlugField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Enter a unique slug'}))
    active = forms.BooleanField(initial=True, required=False)

    def is_valid(self) -> bool:
        id = self.data['id'] if "id" in self.data else None

        if "slug" in self.data and not SportsQueries.is_unique_slug(self.data['slug'], id):
            self.add_error('slug', 'Not Unique')

        return super().is_valid()


class EventForm(forms.Form):
    name = forms.CharField(max_length=100)
    slug = forms.SlugField()
    active = forms.BooleanField(initial=True)
    type = forms.ChoiceField(
        choices=[('preplay', 'Preplay'), ('inplay', 'Inplay')])
    sport = forms.IntegerField()
    status = forms.ChoiceField(choices=[('Pending', 'Pending'), (
        'Started', 'Started'), ('Ended', 'Ended'), ('Cancelled', 'Cancelled')])
    scheduled_start = forms.DateTimeField()
    actual_start = forms.DateTimeField()

    def is_valid(self) -> bool:
        id = self.data['id'] if "id" in self.data else None

        if "slug" in self.data and not EventsQueries.is_unique_slug(self.data['slug'], id):
            self.add_error('slug', 'Not Unique')

        if "sport" in self.data and not SportsQueries.find(self.data['sport']):
            self.add_error('sport', 'Sport with this ID does not exist')

        return super().is_valid()


class SelectionForm(forms.Form):
    name = forms.CharField(max_length=100)
    event = forms.IntegerField()
    price = forms.DecimalField(max_digits=5, decimal_places=2)
    active = forms.BooleanField(initial=True)
    outcome = forms.ChoiceField(choices=[(
        'Unsettled', 'Unsettled'), ('Void', 'Void'), ('Lose', 'Lose'), ('Win', 'Win')])

    def is_valid(self) -> bool:
        if "event" in self.data and not EventsQueries.find(self.data['event']):
            self.add_error('event', 'Event with this ID does not exist')
        return super().is_valid()
