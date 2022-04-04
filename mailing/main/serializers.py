from rest_framework import serializers

from main.models import Client, MailingList, Message, Tag, CodeMobile


class ClientModelSerializer(serializers.ModelSerializer):
    """Serializer for Client"""
    tag = serializers.CharField(min_length=1, max_length=32, allow_blank=True)
    code_mobile = serializers.StringRelatedField()

    class Meta:
        model = Client
        fields = ('id', 'phone', 'tag', 'code_mobile', 'timezone')


class MailingModelSerializer(serializers.ModelSerializer):
    """Serializer for Mailing"""
    tags = serializers.SlugRelatedField(many=True, read_only=False,
                                        slug_field='tag',
                                        queryset=Tag.objects.all())
    code = serializers.SlugRelatedField(many=True, read_only=False,
                                        slug_field='code_mobile',
                                        queryset=CodeMobile.objects.all())
    msg_send_count = serializers.SerializerMethodField('get_msg_send')
    msg_not_send_count = serializers.SerializerMethodField('get_msg_not_send')

    @classmethod
    def get_msg_send(cls, obj):
        return f'{Message.objects.filter(status=True, mailing=obj.id).count()}'

    @classmethod
    def get_msg_not_send(cls, obj):
        return \
            f'{Message.objects.filter(status=False, mailing=obj.id).count()}'

    class Meta:
        model = MailingList
        fields = ('id', 'text_msg', 'start', 'finish', 'tags', 'code',
                  'msg_send_count', 'msg_not_send_count')

    def validate(self, attrs):
        start = attrs.get('start')
        finish = attrs.get('finish')
        if finish <= start:
            raise serializers.ValidationError('Date start >= Date finish')
        return super().validate(attrs)


class MailingDetailSerializer(serializers.ModelSerializer):
    """Serializer for Mailing detail"""
    tags = serializers.SlugRelatedField(many=True, read_only=False,
                                        slug_field='tag',
                                        queryset=Tag.objects.all())
    code = serializers.SlugRelatedField(many=True, read_only=False,
                                        slug_field='code_mobile',
                                        queryset=CodeMobile.objects.all())
    msg_send = serializers.SerializerMethodField('get_msg_send')
    msg_not_send = serializers.SerializerMethodField('get_msg_not_send')

    @classmethod
    def get_detail_message(cls, messages):
        result = []
        for message in messages:
            try:
                tag = message.client.tag.tag
            except:
                tag = None
            client = {
                'id': message.client.id, 'phone': message.client.phone,
                'code_mobile': message.client.code_mobile.code_mobile,
                'tag': tag,
                'timezone': message.client.timezone
            }
            data = {'id': message.id, 'created': message.created,
                    'status': message.status, 'client': client}
            result.append(data)
        return result

    @classmethod
    def get_msg_send(cls, obj):
        messages = Message.objects.filter(status=True, mailing=obj.id)
        return cls.get_detail_message(messages)

    @classmethod
    def get_msg_not_send(cls, obj):
        messages = Message.objects.filter(status=False, mailing=obj.id)
        return cls.get_detail_message(messages)

    class Meta:
        model = MailingList
        fields = ('id', 'text_msg', 'start', 'finish', 'tags', 'code',
                  'msg_send', 'msg_not_send')

    def validate(self, attrs):
        start = attrs.get('start')
        finish = attrs.get('finish')
        if finish <= start:
            raise serializers.ValidationError('Date start >= Date finish')
        return super().validate(attrs)
