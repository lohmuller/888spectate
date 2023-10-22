from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, action
from django.utils.decorators import method_decorator

from ..serializers import SportSerializer
from ..queries.sports_queries import SportsQueries


class SportsView(APIView):

    http_method_names = ['get', 'post', 'patch']
    serializer_classes = SportSerializer
    raw_queries = SportsQueries

    @swagger_auto_schema(
        operation_id='sports_list',
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY,
                              description="Description of the parameter", type=openapi.TYPE_STRING),
            openapi.Parameter('slug', openapi.IN_QUERY,
                              description="Description of the parameter", type=openapi.TYPE_STRING),
            openapi.Parameter('active', openapi.IN_QUERY,
                              description="Description of the parameter", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('active_events_threshold', openapi.IN_QUERY,
                              description="Description of the parameter", type=openapi.TYPE_STRING),

        ],
        responses={200: 'OK'}
    )
    def get(self, request):
        sports = self.raw_queries.list(request.query_params)
        serializer = self.serializer_classes.Model(sports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id='sports_list',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'slug': openapi.Schema(type=openapi.TYPE_STRING),
                'active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            }
        ),
        responses={201: 'Created', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = self.serializer_classes(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        new_id = self.raw_queries.create(serializer.cleaned_data)
        return Response({'id': new_id, **serializer.cleaned_data}, status=status.HTTP_201_CREATED)

    class UsingIdPath(APIView):
        @swagger_auto_schema(
            operation_id='sports_detail',
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'slug': openapi.Schema(type=openapi.TYPE_STRING),
                    'active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                }
            ),
            manual_parameters=[
                openapi.Parameter(
                    name='id',
                    in_=openapi.IN_PATH,
                    type=openapi.TYPE_INTEGER,
                    description='Sport Id',
                    required=True
                )
            ],
            responses={200: 'OK', 400: 'Bad Request', 404: 'Not Found'}
        )
        def patch(self, request, id, *args, **kwargs):

            sport = SportsView.raw_queries.find(id)
            if sport is None or sport.id is None:
                return Response('Not Found', status=status.HTTP_404_NOT_FOUND)

            serializer = SportsView.serializer_classes(
                data={**request.data, 'id': id})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            SportsView.raw_queries.update(id, serializer.cleaned_data)

            return Response(serializer.cleaned_data, status=status.HTTP_200_OK)
