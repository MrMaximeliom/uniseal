from rest_framework import viewsets
from Util.permissions import UnisealPermission
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

# Create your views here.
class  BrochuresViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify brochures by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "title": "title",
        "attachment": "document_url_image",
       }
      Use PUT function by accessing this url:
      /brochures/<brochures'_id>
      Format of data will be as the previous data format for GET function

      """
    from brochures.serializers import BrochuresSerializer

    def get_view_name(self):
        return _("Create/Modify Brochures' Data")

    from brochures.models import Brochures
    queryset = Brochures.objects.all()
    serializer_class = BrochuresSerializer
    permission_classes = [UnisealPermission]

# Dashboard Views
from .models import Brochures
brochures = Brochures.objects.all().order_by("id")
def all_brochures(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(brochures, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        brochures_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        brochures_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        brochures_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'brochures/all_brochures.html',
                  {
                      'title': _('All Brochures'),
                      'all_brochures': 'active',
                      'all_brochures_data': brochures_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )



def add_brochures(request):
    from .forms import BrochuresForm
    if request.method == 'POST':
        form = BrochuresForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f"New Brochure Added: {title}")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = BrochuresForm()


    context = {
        'title': _('Add Brochures'),
        'add_brochures': 'active',
        'form': form,
    }
    return render(request, 'brochures/add_brochures.html', context)

def delete_brochures(request):

    context = {
        'title': _('Delete Brochures'),
        'delete_brochures': 'active',
        'all_brochures': brochures,
    }
    return render(request, 'brochures/delete_brochures.html', context)

def edit_brochures(request):
    context = {
        'title': _('Edit Brochures'),
        'edit_brochures': 'active',
        'all_brochures': brochures,
    }
    return render(request, 'brochures/edit_brochures.html', context)

