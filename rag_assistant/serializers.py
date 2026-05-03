from rest_framework import serializers


class AssistantRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=2000)
