from ..serializers import SelectionSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..queries.selections_queries import SelectionQueries
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class SelectionView(APIView):

    http_method_names = ['get', 'post', 'patch']
    serializer_classes = [SelectionSerializer]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY,
                              description="Name of the outcome", type=openapi.TYPE_STRING),
            openapi.Parameter('event', openapi.IN_QUERY,
                              description="ID of the event", type=openapi.TYPE_INTEGER),
            openapi.Parameter('price', openapi.IN_QUERY, description="Price of the outcome", type=openapi.TYPE_STRING,
                              format=openapi.FORMAT_DECIMAL),
            openapi.Parameter('active', openapi.IN_QUERY,
                              description="Active status of the outcome", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('outcome', openapi.IN_QUERY, description="Outcome status",
                              type=openapi.TYPE_STRING, enum=['Unsettled', 'Void', 'Lose', 'Win']),
        ],
        responses={200: 'OK'}
    )
    def get(self, request):
        query_params = request.query_params
        sports = SelectionQueries.list(
            query_params)
        serializer = SelectionSerializer.Model(sports, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'event': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                'price': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DECIMAL, example="3.3"),
                'active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'outcome': openapi.Schema(type=openapi.TYPE_STRING, enum=['Unsettled', 'Void', 'Lose', 'Win'])
            },
            required=['name', 'event', 'price', 'active', 'outcome'],
            responses={201: 'CREATED', 400: 'Bad Request'}
        )
    )
    def post(self, request):
        serializer = SelectionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        new_id = SelectionQueries.create(serializer.cleaned_data)
        return Response({'id': new_id, **serializer.cleaned_data}, status=status.HTTP_201_CREATED)

    class UsingIdPath(APIView):
        @swagger_auto_schema(
            operation_id="id",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'event': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    'price': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DECIMAL, example="3.3"),
                    'active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'outcome': openapi.Schema(type=openapi.TYPE_STRING, enum=['Unsettled', 'Void', 'Lose', 'Win'])
                },
                required=['name', 'event', 'price', 'active', 'outcome']
            ),
            manual_parameters=[
                openapi.Parameter(
                    name='id',  # Nome do parâmetro da URL
                    in_=openapi.IN_PATH,  # Especifica que é um parâmetro da URL
                    # Tipo de dado do parâmetro (pode ser alterado conforme necessário)
                    type=openapi.TYPE_INTEGER,
                    description='ID do esporte',  # Descrição do parâmetro
                    required=True  # Especifica se o parâmetro é obrigatório ou opcional
                )
            ],
            responses={200: 'OK', 400: 'Bad Request'}
        )
        def patch(self, request, id, *args, **kwargs):
            selection = SelectionQueries.find(id)
            if selection is None or selection.id is None:
                return Response('Not Found', status=status.HTTP_404_NOT_FOUND)

            serializer = SelectionSerializer(data={**request.data, 'id': id})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            SelectionQueries.update(id, serializer.cleaned_data)
            return Response(serializer.cleaned_data, status=status.HTTP_200_OK)
