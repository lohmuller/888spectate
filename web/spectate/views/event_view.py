from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..swagger_params import event_query_parameters, event_request_body
from ..serializers import EventSerializer
from ..queries.events_queries import EventsQueries
from ..forms import EventForm


class EventView(APIView):

    http_method_names = ['get', 'post', 'patch']

    @swagger_auto_schema(
        manual_parameters=event_query_parameters(),
        responses={200: 'OK', 400: 'Bad Request'}
    )
    def get(self, request):
        query_params = request.query_params
        events = EventsQueries.list(
            query_params)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="create_event",
        request_body=event_request_body(),
        responses={201: 'CREATED', 400: 'Bad Request'}
    )
    def post(self, request):
        form = EventForm(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        new_id = EventsQueries.create(form.cleaned_data)
        return Response({'id': new_id, **form.cleaned_data}, status=status.HTTP_201_CREATED)

    class UsingIdPath(APIView):
        @swagger_auto_schema(
            operation_id="id",
            request_body=event_request_body(),
            manual_parameters=[
                openapi.Parameter(
                    name='id',
                    in_=openapi.IN_PATH,
                    type=openapi.TYPE_INTEGER,
                    description='Event ID',
                    required=True,
                    example=1
                )
            ],
            responses={200: 'OK', 400: 'Bad Request', 404: 'Not Found'}
        )
        def patch(self, request, id, *args, **kwargs):
            event = EventsQueries.find(id)

            if event is None or event.id is None:
                return Response('Not Found', status=status.HTTP_404_NOT_FOUND)

            form = EventForm(data={'id': id, **request.data})
            if not form.is_valid():
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
            EventsQueries.update(id, form.cleaned_data)
            return Response(form.cleaned_data, status=status.HTTP_200_OK)
