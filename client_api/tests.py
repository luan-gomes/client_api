from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from client_api.models import Client


class ClientAPITestCase(APITestCase):
    CLIENT_JSON = {
        "company_name": "My company",
        "phone": "5571998989898",
        "address": {
            "address": "Rua Amaralina",
            "number": 780,
            "zip_code": "44000000",
            "city": "Salvador",
            "state": "Bahia",
            "country": "Brazil"
        },
        "registration_date": "1996-07-16",
        "declared_billing": 100000.20,
        "bank_accounts": [
            {
                "agency": "0002",
                "account_number": "000254",
                "bank": "Pag bank"
            }
        ]
    }

    def create_client(self):
        response = self.client.post(
            reverse('clients_list'),
            self.CLIENT_JSON,
            format="json"
        )
        return response


class TestListCreateClient(ClientAPITestCase):
    def test_get_all_clients(self):
        response = self.client.get(reverse('clients_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_create_client(self):
        response = self.create_client()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 1)

    def test_create_client_with_different_json_format(self):
        different_json = {
            'razo_social': 1254782,
            'telefone': '55759999999',
            'endereco': 'Street, 45'
        }
        response = self.client.post(
            reverse('clients_list'),
            different_json,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestClientDetails(ClientAPITestCase):

    def test_get_one_client(self):
        client_response = self.create_client()
        client_id = client_response.data['id']
        response = self.client.get(
            reverse('client_details', kwargs={'id': client_id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], client_id)

    def test_update_client(self):
        client_response = self.create_client()
        client_id = client_response.data['id']
        updated_json = {
            "id": client_id,
            "company_name": "My new company",
            "phone": "5571998989898",
            "address": {
                "address": "Rua Amaralina",
                "number": 780,
                "zip_code": "44000000",
                "city": "Salvador",
                "state": "Bahia",
                "country": "Brazil"
            },
            "registration_date": "1996-07-16",
            "declared_billing": 100000.20,
            "bank_accounts": [
                {
                    "agency": "0002",
                    "account_number": "000254",
                    "bank": "Pag bank"
                }
            ]
        }
        response = self.client.put(
            reverse('client_details', kwargs={'id': client_id}),
            updated_json,
            format="json"
        )

        client_obj = Client.objects.get(pk=client_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(client_obj.company_name, "My new company")

    def test_delete_client(self):
        client_response = self.create_client()
        client_id = client_response.data['id']
        previous_db_count = Client.objects.all().count()
        response = self.client.delete(
            reverse('client_details', kwargs={'id': client_id})
        )
        current_db_count = Client.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(current_db_count, previous_db_count-1)



