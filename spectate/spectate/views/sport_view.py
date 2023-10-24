from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..serializers import SportSerializer
from ..forms import SportForm as SportForm
from ..queries.sports_queries import SportsQueries


class SportsView(APIView):

    http_method_names = ['get', 'post', 'patch']

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
        sports = SportsQueries.list(request.query_params)
        serializer = SportSerializer(sports, many=True)
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
        form = SportForm(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        new_id = SportsQueries.create(form.cleaned_data)
        return Response({'id': new_id, **form.cleaned_data}, status=status.HTTP_201_CREATED)

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

            sport = SportsQueries.find(id)
            if sport is None or sport.id is None:
                return Response('Not Found', status=status.HTTP_404_NOT_FOUND)

            form = SportForm(
                data={**request.data, 'id': id})
            if not form.is_valid():
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
            SportsQueries.update(id, form.cleaned_data)

            return Response(form.cleaned_data, status=status.HTTP_200_OK)
