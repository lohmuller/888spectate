from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..serializers import EventSerializer
from ..queries.events_queries import EventsQueries
from ..forms import EventForm


class EventView(APIView):

    http_method_names = ['get', 'post', 'patch']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY,
                              description="Name parameter", type=openapi.TYPE_STRING),
            openapi.Parameter('slug', openapi.IN_QUERY,
                              description="Slug parameter", type=openapi.TYPE_STRING),
            openapi.Parameter('active', openapi.IN_QUERY,
                              description="Active parameter", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('type', openapi.IN_QUERY,
                              description="Type parameter", type=openapi.TYPE_STRING, enum=['preplay', 'inplay']),
            openapi.Parameter('sport', openapi.IN_QUERY,
                              description="Sport parameter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('status', openapi.IN_QUERY,
                              description="Status parameter", type=openapi.TYPE_STRING, enum=['Pending', 'Started', 'Ended', 'Cancelled']),
            openapi.Parameter('scheduled_start_after', openapi.IN_QUERY,
                              description="Scheduled Start parameter", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            openapi.Parameter('scheduled_start_before', openapi.IN_QUERY,
                              description="Scheduled Start parameter", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            openapi.Parameter('actual_start_after', openapi.IN_QUERY,
                              description="Actual Start parameter", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, nullable=True),
            openapi.Parameter('actual_start_before', openapi.IN_QUERY,
                              description="Actual Start parameter", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, nullable=True),
            openapi.Parameter('active_selections_threshold', openapi.IN_QUERY,
                              description="Active selections threshold parameter", type=openapi.TYPE_INTEGER),

        ],
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'slug': openapi.Schema(type=openapi.TYPE_STRING),
                'active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['preplay', 'inplay']),
                'sport': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['Pending', 'Started', 'Ended', 'Cancelled']),
                'scheduled_start': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                'actual_start': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, nullable=True),
            }
        ),
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
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'slug': openapi.Schema(type=openapi.TYPE_STRING),
                    'active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['preplay', 'inplay']),
                    'sport': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['Pending', 'Started', 'Ended', 'Cancelled']),
                    'scheduled_start': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                    'actual_start': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, nullable=True),
                }
            ),
            manual_parameters=[
                openapi.Parameter(
                    name='id',
                    in_=openapi.IN_PATH,
                    type=openapi.TYPE_INTEGER,
                    description='Event ID',
                    required=True
                )
            ],
            responses={200: 'OK'}
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
