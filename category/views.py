from rest_framework import viewsets

from Util.permissions import  UnisealPermission

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render

class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify categories' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id": 12,
     "name":"category_name",
     }
     Use other functions by accessing this url:
     category/<category's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Categories")

    from .serializers import CategorySerializer
    serializer_class = CategorySerializer
    from .models import Category
    permission_classes = [UnisealPermission]
    queryset = Category.objects.all()
#Views for dashboard
from category.models import Category
categories = Category.objects.all()
def all_categories(request):
    context = {
        'title': _('All Categories'),
        'all_categories': 'active',
        'all_categories_data': categories,
    }
    return render(request, 'category/all_categories.html', context)

def add_categories(request):

    context = {
        'title': _('Add Categories'),
        'add_categories': 'active',
        'all_categories': categories,
    }
    return render(request, 'category/add_categories.html', context)

def delete_categories(request):

    context = {
        'title': _('Delete Categories'),
        'delete_categories': 'active',
        'all_categories': categories,
    }
    return render(request, 'category/delete_categories.html', context)

def edit_categories(request):
    context = {
        'title': _('Edit Category'),
        'edit_categories': 'active',
        'all_categories': categories,
    }
    return render(request, 'category/edit_categories.html', context)
