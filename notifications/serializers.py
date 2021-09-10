from rest_framework import serializers

class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import Notifications
        model = Notifications
        # fields = '__all__'
        exclude = ('slug',)

class TokensSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import TokenIDs
        model = TokenIDs
        # fields = '__all__'
        exclude = ('slug',)
