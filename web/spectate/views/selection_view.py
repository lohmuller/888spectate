from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..swagger_params import selection_query_parameters, selection_request_body
from ..serializers import SelectionSerializer
from ..queries.selections_queries import SelectionQueries
from ..forms import SelectionForm as SelectionForm


class SelectionView(APIView):

    http_method_names = ['get', 'post', 'patch']

    @swagger_auto_schema(
        manual_parameters=selection_query_parameters(),
        responses={200: 'OK'}
    )
    def get(self, request):
        query_params = request.query_params
        selection = SelectionQueries.list(
            query_params)
        serializer = SelectionSerializer(selection, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=selection_request_body(),
        responses={201: 'CREATED', 400: 'Bad Request'}
    )
    def post(self, request):
        form = SelectionForm(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        new_id = SelectionQueries.create(form.cleaned_data)
        return Response({'id': new_id, **form.cleaned_data}, status=status.HTTP_201_CREATED)

    class UsingIdPath(APIView):
        @swagger_auto_schema(
            operation_id="id",
            request_body=selection_request_body(),
            manual_parameters=[
                openapi.Parameter(
                    name='id',
                    in_=openapi.IN_PATH,
                    type=openapi.TYPE_INTEGER,
                    description='Selection ID',
                    required=True
                )
            ],
            responses={200: 'OK', 400: 'Bad Request'}
        )
        def patch(self, request, id, *args, **kwargs):
            selection = SelectionQueries.find(id)
            if selection is None or selection.id is None:
                return Response('Not Found', status=status.HTTP_404_NOT_FOUND)

            form = SelectionForm(data={**request.data, 'id': id})
            if not form.is_valid():
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
            SelectionQueries.update(id, form.cleaned_data)
            return Response(form.cleaned_data, status=status.HTTP_200_OK)
