from rest_framework import viewsets
from Util.permissions import UnisealPermission
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


# Create your views here.
class  SliderViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify slider images by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "image": "path_to_image",
        "link": "url",
    }
    Use PUT function by accessing this url:
    /slider/<slider's_id>
    Format of data will be as the previous data format for GET function

      """
    from .serializers import SliderSerializer

    def get_view_name(self):
        return _("Create/Modify Slider's Data")

    from .models import Slider
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [UnisealPermission]

#Views for dashboard
from slider.models import Slider
sliders = Slider.objects.all()
def all_sliders(request):
    context = {
        'title': _('All Sliders'),
        'all_sliders': 'active',
        'all_sliders_data': sliders,
    }
    return render(request, 'slider/all_sliders.html', context)

def add_sliders(request):

    context = {
        'title': _('Add Sliders'),
        'add_sliders': 'active',
        'all_sliders': sliders,
    }
    return render(request, 'slider/add_sliders.html', context)

def delete_sliders(request):

    context = {
        'title': _('Delete Sliders'),
        'delete_sliders': 'active',
        'all_sliders': sliders,
    }
    return render(request, 'slider/delete_sliders.html', context)

def edit_sliders(request):
    context = {
        'title': _('Edit Slider'),
        'edit_sliders': 'active',
        'all_sliders': sliders,
    }
    return render(request, 'slider/edit_sliders.html', context)
