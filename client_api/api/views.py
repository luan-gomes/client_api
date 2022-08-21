from client_api.models import Client
from client_api.api.serializers import ClientSerializer
from rest_framework.parsers import JSONParser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ClientsAPIView(ListCreateAPIView):
    serializer_class = ClientSerializer
    parser_classes = [JSONParser]

    def get_queryset(self):
        return Client.objects.all()


class ClientDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    parser_classes = [JSONParser]
    lookup_field = 'id'

    def get_queryset(self):
        return Client.objects.all()
