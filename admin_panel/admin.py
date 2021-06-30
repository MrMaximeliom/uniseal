from django.contrib import admin
from .models import ManageProducts,ManageSolution,ManageProjects,ManageBrochures,ManageSellingPoints
# Register your models here.

admin.site.register(ManageBrochures)
admin.site.register(ManageProjects)
admin.site.register(ManageProducts)
admin.site.register(ManageSolution)
admin.site.register(ManageSellingPoints)