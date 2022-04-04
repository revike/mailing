from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from main.models import Client, MailingList, Tag, CodeMobile
from main.serializers import ClientModelSerializer, MailingModelSerializer, \
    MailingDetailSerializer
from main.tasks import mailing_start


class ClientModelViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                         GenericViewSet, CreateModelMixin, DestroyModelMixin):
    """Client model view set"""
    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer

    @staticmethod
    def tag_create_or_update(serializer):
        data = serializer.validated_data
        tag_data = data.get('tag')
        if tag_data:
            tag = Tag.objects.filter(tag=tag_data).first()
            if not tag:
                tag = Tag.objects.create(tag=tag_data)
        else:
            tag = None
        serializer.validated_data['tag'] = tag

        code_mobile = data.get('phone')[1:4]
        code = CodeMobile.objects.filter(code_mobile=code_mobile).first()
        if not code:
            code = CodeMobile.objects.create(code_mobile=code_mobile)
        serializer.validated_data['code_mobile'] = code

        return serializer.save()

    def perform_create(self, serializer):
        self.tag_create_or_update(serializer)

    def perform_update(self, serializer):
        self.tag_create_or_update(serializer)


class MailingModelViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                          GenericViewSet, CreateModelMixin, DestroyModelMixin):
    """Mailing model view set"""
    queryset = MailingList.objects.all()
    serializer_class = MailingModelSerializer

    def get_serializer_class(self):
        if self.__dict__['detail']:
            return MailingDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        create = super().perform_create(serializer)
        mailing = serializer.data
        mailing_start.apply_async(countdown=1, args=[mailing])
        return create

    def perform_update(self, serializer):
        update = super().perform_update(serializer)
        mailing = serializer.data
        mailing_start.apply_async(countdown=1, args=[mailing])
        return update
