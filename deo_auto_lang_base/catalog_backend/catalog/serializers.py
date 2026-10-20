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
    yearFrom = serializers.IntegerField(source="year_from", allow_null=True)
    yearTo = serializers.IntegerField(source="year_to", allow_null=True)


class PublicReviewCandidateSerializer(VerifiedConfigurationSerializer):
    reviewStatus = serializers.CharField(source="review_status")
