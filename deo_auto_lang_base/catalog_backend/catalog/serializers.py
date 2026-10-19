from rest_framework import serializers


class VerifiedConfigurationSerializer(serializers.Serializer):
    id = serializers.CharField()
    make = serializers.CharField()
    model = serializers.CharField()
    generation = serializers.CharField()
    region = serializers.CharField()
    systemType = serializers.CharField(source="system_type")
    hardwareRevision = serializers.CharField(source="hardware_revision")
    softwareVersion = serializers.CharField(source="software_version")
    verifiedAt = serializers.DateField(source="verified_at", allow_null=True)
    limitations = serializers.CharField()
