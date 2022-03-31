from django.contrib import admin

from mailing.main.models import Client, MailingList, Message

admin.site.register(Client)
admin.site.register(MailingList)
admin.site.register(Message)
