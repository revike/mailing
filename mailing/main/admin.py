from django.contrib import admin

from main.models import Client, MailingList, Message, Tag, CodeMobile

admin.site.register(Client)
admin.site.register(MailingList)
admin.site.register(Message)
admin.site.register(Tag)
admin.site.register(CodeMobile)
