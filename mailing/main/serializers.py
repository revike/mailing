from rest_framework import serializers

from main.models import Client, MailingList, Message, Tag, CodeMobile


class TagModelSerializer(serializers.ModelSerializer):
    """Serializer for Tag"""

    class Meta:
        model = Tag
        fields = '__all__'


class CodeModelSerializer(serializers.ModelSerializer):
    """Serializer for Code mobile"""

    class Meta:
        model = CodeMobile
        fields = '__all__'


class ClientModelSerializer(serializers.ModelSerializer):
    """Serializer for Client"""
    tag = serializers.CharField(min_length=1, max_length=32, allow_blank=True)
    code_mobile = serializers.StringRelatedField()

    class Meta:
        model = Client
        fields = ('id', 'phone', 'tag', 'code_mobile', 'timezone')


class MailingModelSerializer(serializers.ModelSerializer):
    """Serializer for Mailing"""

    class Meta:
        model = MailingList
        fields = '__all__'

    def validate(self, attrs):
        start = attrs.get('start')
        finish = attrs.get('finish')
        if finish <= start:
            raise serializers.ValidationError('Date start >= Date finish')
        return super().validate(attrs)


class MessageModelSerializer(serializers.ModelSerializer):
    """Serializer for Massage"""

    class Meta:
        model = Message
        fields = '__all__'
