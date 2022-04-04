from datetime import datetime, timedelta

import pytz
from django.core.management import call_command
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, \
    APIClient

from authenticated.models import User
from mailing.settings import TIME_ZONE
from main.models import Client, MailingList
from main.views import ClientModelViewSet


class TestClientViewSet(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.username = 'user_admin'
        self.password = 'admin'
        self.admin = User.objects.create_superuser('user_admin',
                                                   'admin@admin.com',
                                                   'admin')
        self.url_client = '/api/client/'
        self.url_mailing = '/api/mailing/'

    def test_get_clients(self):
        request = self.factory.get(self.url_client)
        view = ClientModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = self.factory.get(self.url_client)
        force_authenticate(request, self.admin)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.url_client)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url_client)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_clients(self):
        new_client = {
            'phone': '7999999',
            'tag': 'my_tag',
            'timezone': 'Europe/Moscow'
        }
        clients_count_start = Client.objects.all().count()
        response = self.client.post(self.url_client, new_client, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url_client, new_client, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        clients_count_finish = Client.objects.all().count()
        self.assertEqual(clients_count_start, clients_count_finish)

        clients_count_start = Client.objects.all().count()
        new_client['phone'] = '79998887766'
        response = self.client.post(self.url_client, new_client, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        clients_count_finish = Client.objects.all().count()
        self.assertEqual(clients_count_start + 1, clients_count_finish)

    def test_get_client(self):
        clients = Client.objects.all()
        for client in clients:
            request = self.factory.get(f'{self.url_client}{client.id}/')
            view = ClientModelViewSet.as_view({'get': 'list'})
            response = view(request)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            response = self.client.get(f'{self.url_client}{client.id}/')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            self.client.login(username=self.username, password=self.password)

            response = self.client.get(f'{self.url_client}{client.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.client.logout()

    def test_put_client(self):
        clients = Client.objects.all()
        for client in clients:
            response = self.client.put(f'{self.url_client}{client.id}/')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            self.client.login(username=self.username, password=self.password)

            response = self.client.put(f'{self.url_client}{client.id}/')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            data = {
                'phone': client.phone,
                'tag': client.tag.tag,
                'timezone': client.timezone
            }

            new_data = data.copy()
            new_data['tag'] = f'{client.tag.tag}_test'
            self.assertNotEqual(data, new_data)

            response = self.client.put(f'{self.url_client}{client.id}/',
                                       new_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            client_tag = data['tag']
            self.assertNotEqual(client_tag, client.tag)

            self.client.logout()

    def test_delete_client(self):
        clients = Client.objects.all()
        clients_count_start = clients.count()
        for client in clients:
            request = self.factory.delete(f'{self.url_client}{client.id}/')
            view = ClientModelViewSet.as_view({'get': 'list'})
            response = view(request)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            response = self.client.delete(f'{self.url_client}{client.id}/')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            self.client.login(username=self.username, password=self.password)

            response = self.client.delete(f'{self.url_client}{client.id}/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            self.client.logout()

        clients_count_finish = Client.objects.all().count()
        self.assertNotEqual(clients_count_start, clients_count_finish)
        self.assertEqual(clients_count_finish, 0)

    def test_get_mailings(self):
        response = self.client.get(self.url_mailing)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url_mailing)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_mailing(self):
        date_time = datetime.now(tz=pytz.timezone(TIME_ZONE))
        new_mailing = {
            'text_msg': 'test',
            'start': f'{date_time}',
            'finish': f'{date_time}',
            'tags': [],
            'code': []
        }
        mailing_count_start = MailingList.objects.all().count()
        response = self.client.post(self.url_mailing, new_mailing,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url_mailing, new_mailing,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mailing_count_finish = MailingList.objects.all().count()
        self.assertEqual(mailing_count_start, mailing_count_finish)

        mailing_count_start = MailingList.objects.all().count()
        new_mailing['start'] = \
            f'{datetime.now(tz=pytz.timezone(TIME_ZONE)) - timedelta(days=1)}'
        new_mailing['finish'] = \
            f'{datetime.now(tz=pytz.timezone(TIME_ZONE)) + timedelta(days=1)}'
        response = self.client.post(self.url_mailing, new_mailing,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mailing_count_finish = MailingList.objects.all().count()
        self.assertNotEqual(mailing_count_start, mailing_count_finish)

    def test_get_mailing(self):
        mailings = MailingList.objects.all()
        for mailing in mailings:
            response = self.client.get(f'{self.url_mailing}{mailing.id}/')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            self.client.login(username=self.username, password=self.password)

            response = self.client.get(f'{self.url_mailing}{mailing.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.client.logout()

    def test_put_mailing(self):
        mailings = MailingList.objects.all()
        for mailing in mailings:
            response = self.client.put(f'{self.url_mailing}{mailing.id}/')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            self.client.login(username=self.username, password=self.password)

            response = self.client.put(f'{self.url_mailing}{mailing.id}/')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            data = {
                'text_msg': mailing.text_msg,
                'start': f'{mailing.start}',
                'finish': f'{mailing.finish}',
                'tags': [],
                'code': []
            }

            new_data = data.copy()
            new_data['text_msg'] = f'{mailing.text_msg}_test'
            self.assertNotEqual(data, new_data)

            response = self.client.put(f'{self.url_mailing}{mailing.id}/',
                                       new_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            text_msg = data['text_msg']
            new_text_msg = MailingList.objects.filter(
                id=mailing.id).first().text_msg
            self.assertNotEqual(text_msg, new_text_msg)

            self.client.logout()

    def test_delete_mailing(self):
        mailings = MailingList.objects.all()
        mailings_count_start = mailings.count()
        for mailing in mailings:
            response = self.client.delete(f'{self.url_mailing}{mailing.id}/')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            self.client.login(username=self.username, password=self.password)

            response = self.client.delete(f'{self.url_mailing}{mailing.id}/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            self.client.logout()

        mailings_count_finish = MailingList.objects.all().count()
        self.assertNotEqual(mailings_count_start, mailings_count_finish)
        self.assertEqual(mailings_count_finish, 0)
