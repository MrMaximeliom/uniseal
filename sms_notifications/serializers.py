from rest_framework import serializers

# Create your models here.
class SMSGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import SMSGroups
        model = SMSGroups
        fields = "__all__"


class SMSNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import SMSNotification
        model = SMSNotification
        fields = "__all__"


class SMSContactsSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import SMSContacts
        model = SMSContacts
        fields = "__all__"


