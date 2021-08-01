from rest_framework import serializers


class ProjectApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        from project.models import Application
        model = Application
        fields = "__all__"
