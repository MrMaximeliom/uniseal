from rest_framework import serializers

class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import Notifications
        model = Notifications
        exclude = ('slug',)
        lookup_field = 'slug'

class TokensSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import TokenIDs
        model = TokenIDs
        exclude = ('slug',)
