import pytz
from django.core.validators import RegexValidator
from django.db import models


class Client(models.Model):
    """Model client"""

    class Meta:
        verbose_name_plural = 'Clients'
        verbose_name = 'Clients'

    TIMEZONE = pytz.all_timezones
    phone_regex = RegexValidator(regex=r"^7\d{10}$")
    code_regex = RegexValidator(regex=r"^\d{3}$")

    phone = models.CharField(validators=[phone_regex], max_length=9,
                             unique=True, verbose_name='Phone number')
    code_mobile = models.CharField(validators=[code_regex], max_length=3,
                                   verbose_name='code mobile operator')
    tag = models.CharField(max_length=32, blank=True, verbose_name='tag')
    timezone = models.CharField(max_length=128, choices=TIMEZONE,
                                verbose_name='timezone')

    def __str__(self):
        return f'{self.phone} - {self.tag}'


class MailingList(models.Model):
    """Model mailing list"""

    class Meta:
        verbose_name_plural = 'Mailing list'
        verbose_name = 'Mailing list'

    """Model mailing list"""
    text_msg = models.CharField(max_length=512, verbose_name='message text')
    start = models.DateTimeField(verbose_name='start mailing')
    finish = models.DateTimeField(verbose_name='finish mailing')

    def __str__(self):
        return f'{self.text_msg}'


class Message(models.Model):
    """Model message"""

    class Meta:
        verbose_name_plural = 'Messages'
        verbose_name = 'Messages'

    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    status = models.BooleanField(default=False, db_index=True,
                                 verbose_name='send')
    mailing = models.ForeignKey(MailingList, on_delete=models.CASCADE,
                                verbose_name='mailing')
    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               verbose_name='client')

    def __str__(self):
        return f'{self.mailing} - {self.client}'
