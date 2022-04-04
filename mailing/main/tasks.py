import pytz
from datetime import datetime

import requests
from celery import shared_task

from mailing.settings import JWT_TOKEN, MAILING_SERVER
from main.models import Client, MailingList, Message


@shared_task()
def mailing_start(data):
    try:
        start_utc = datetime.strptime(
            ' '.join(data['start'].split('T')), '%Y-%m-%d %H:%M:%S%z')
        start = datetime.strptime(f'{start_utc.date()} {start_utc.time()}',
                                  '%Y-%m-%d %H:%M:%S')
        finish_utc = datetime.strptime(
            ' '.join(data['finish'].split('T')), '%Y-%m-%d %H:%M:%S%z')
        finish = datetime.strptime(f'{finish_utc.date()} {finish_utc.time()}',
                                   '%Y-%m-%d %H:%M:%S')
    except ValueError:
        start_utc = datetime.strptime(
            ' '.join(data['start'].split('T')), '%Y-%m-%d %H:%M:%S.%f%z')
        start = datetime.strptime(f'{start_utc.date()} {start_utc.time()}',
                                  '%Y-%m-%d %H:%M:%S.%f')
        finish_utc = datetime.strptime(
            ' '.join(data['finish'].split('T')), '%Y-%m-%d %H:%M:%S.%f%z')
        finish = datetime.strptime(f'{finish_utc.date()} {finish_utc.time()}',
                                   '%Y-%m-%d %H:%M:%S.%f')
    clients = Client.objects.all()
    if data['tags']:
        clients = clients.filter(tag__tag__in=data['tags'])
    if data['code']:
        clients = clients.filter(code_mobile__code_mobile__in=data['code'])

    for client in clients:
        client_date_time_now = datetime.now(tz=pytz.timezone(client.timezone))
        client_now = datetime.strptime(
            f'{client_date_time_now.date()} {client_date_time_now.time()}',
            '%Y-%m-%d %H:%M:%S.%f'
        )
        client_id = client.id
        if start < client_now < finish:
            mailing_task.apply_async(countdown=1, args=[data, client_id])
        elif client_now < start:
            run_mailing = int((start - client_now).total_seconds())
            mailing_task.apply_async(
                countdown=run_mailing, args=[data, client_id])


@shared_task()
def mailing_task(data, client_id, status=False):
    mailing = MailingList.objects.filter(id=data['id']).first()
    client = Client.objects.filter(id=client_id).first()

    data_request = {
        "id": int(data['id']),
        "phone": int(client.phone),
        "text": data['text_msg']
    }
    headers = {
        'Authorization': JWT_TOKEN,
        'Content-Type': 'application/json'
    }
    response = requests.post(url=f'{MAILING_SERVER}/{data_request["id"]}',
                             json=data_request, headers=headers)
    if response.status_code == 200:
        result_server = {'code': 0, 'message': 'OK'}
        if result_server == response.json():
            status = True
    return Message.objects.create(
        mailing=mailing, client=client, status=status)
