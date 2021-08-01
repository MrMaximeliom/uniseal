from django.contrib import admin
from .models import Project,ProjectImages,ProjectVideos
# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectImages)
admin.site.register(ProjectVideos)
