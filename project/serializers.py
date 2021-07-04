from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Project
        model = Project
        fields = "__all__"


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ProjectImages
        model = ProjectImages
        fields = "__all__"


class ProjectVideoSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ProjectVideos
        model = ProjectVideos
        fields = "__all__"

class ProjectSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ProjectSolutions
        model = ProjectSolutions
        fields = "__all__"