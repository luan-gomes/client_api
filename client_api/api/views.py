from client_api.models import Client, Address
from client_api.api.serializers import ClientSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def client_list(request, format=None):
    if request.method == 'GET':
        clients = Client.objects.all()
        client_serializer = ClientSerializer(clients, many=True)
        return Response(client_serializer.data)

    if request.method == 'POST':
        client_serializer = ClientSerializer(data=request.data)
        if client_serializer.is_valid():
            client_serializer.save()
            return Response(client_serializer.data, status=status.HTTP_201_CREATED)
        return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def client_details(request, id, format=None):
    try:
        client = Client.objects.get(pk=id)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        client_serializer = ClientSerializer(client)
        return Response(client_serializer.data)
    elif request.method == 'PUT':
        client_serializer = ClientSerializer(client, data=request.data)
        if client_serializer.is_valid():
            client_serializer.save()
            return Response(client_serializer.data, status=status.HTTP_200_OK)
        return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        address_id = client.address.id
        client.delete()
        Address.objects.get(pk=address_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
