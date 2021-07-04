from rest_framework import serializers

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Solution
        model = Solution
        fields = "__all__"

class SolutionImagesSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import SolutionImages
        model = SolutionImages
        fields = "__all__"

class SolutionVideosSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import SolutionVideos
        model = SolutionVideos
        fields = "__all__"