from rest_framework import serializers


class APIExceptionSerializer(serializers.Serializer):
    status_code = serializers.IntegerField(read_only=True)
    default_detail = serializers.CharField(read_only=True)
    default_code = serializers.CharField(read_only=True)
