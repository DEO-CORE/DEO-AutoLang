from rest_framework import serializers


class CompatibilityRequestSerializer(serializers.Serializer):
    make = serializers.CharField(min_length=2, max_length=80, trim_whitespace=True)
    model = serializers.CharField(min_length=1, max_length=120, trim_whitespace=True)
    year = serializers.IntegerField(
        min_value=1980, max_value=2100, required=False, allow_null=True
    )
    region = serializers.CharField(
        max_length=80, required=False, allow_null=True, allow_blank=True
    )
    systemType = serializers.ChoiceField(
        choices=["factory", "aftermarket", "unknown"], required=False, allow_null=True
    )
    hardwareRevision = serializers.CharField(
        max_length=120, required=False, allow_null=True, allow_blank=True
    )
    softwareVersion = serializers.CharField(
        max_length=120, required=False, allow_null=True, allow_blank=True
    )
    details = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    consentAccepted = serializers.BooleanField()

    def to_internal_value(self, data):
        unexpected = set(data.keys()) - set(self.fields)
        if unexpected:
            raise serializers.ValidationError(
                {
                    key: "Поле не поддерживается. Не отправляйте VIN и персональные данные."
                    for key in unexpected
                }
            )
        values = super().to_internal_value(data)
        if any(
            token in (values.get("details") or "").lower()
            for token in ("vin", "госномер", "пароль", "token", "токен")
        ):
            raise serializers.ValidationError(
                {"details": "Не указывайте VIN, госномер, пароли или токены."}
            )
        return values


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
