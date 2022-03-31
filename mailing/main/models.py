import pytz
from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    """Model Tag"""

    class Meta:
        verbose_name_plural = 'Tags'
        verbose_name = 'Tags'

    tag = models.CharField(max_length=32, verbose_name='tag')

    def __str__(self):
        return f'{self.tag}'


class CodeMobile(models.Model):
    """Model Code Mobile"""

    class Meta:
        verbose_name_plural = 'Code mobile'
        verbose_name = 'Code mobile'

    code_regex = RegexValidator(regex=r"^9\d{2}$")
    code_mobile = models.CharField(validators=[code_regex], max_length=3,
                                   verbose_name='code mobile operator')

    def __str__(self):
        return f'{self.code_mobile}'


class Client(models.Model):
    """Model client"""

    class Meta:
        verbose_name_plural = 'Clients'
        verbose_name = 'Clients'

    TIMEZONE = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    phone_regex = RegexValidator(regex=r"^7\d{10}$")

    phone = models.CharField(validators=[phone_regex], max_length=11,
                             unique=True, verbose_name='Phone number')
    code_mobile = models.ForeignKey(CodeMobile, on_delete=models.PROTECT,
                                    verbose_name='code mobile operator')
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True,
                            verbose_name='tag')
    timezone = models.CharField(max_length=128, choices=TIMEZONE,
                                verbose_name='timezone')

    def __str__(self):
        return f'{self.phone} - {self.tag}'


class MailingList(models.Model):
    """Model mailing list"""

    class Meta:
        verbose_name_plural = 'Mailing list'
        verbose_name = 'Mailing list'

    text_msg = models.CharField(max_length=512, verbose_name='message text')
    start = models.DateTimeField(verbose_name='start mailing')
    finish = models.DateTimeField(verbose_name='finish mailing')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='tags')
    code = models.ManyToManyField(CodeMobile, blank=True,
                                  verbose_name='code mobile')

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
