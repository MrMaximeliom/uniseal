import requests
from django.shortcuts import render
from rest_framework import viewsets
# from Util.permissions import UnisealPermission
from rest_framework.permissions import IsAdminUser

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

class  SMSGroupsViewSet(viewsets.ModelViewSet):
    """
          API endpoint that allows to add or modify sms groups data by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "name":"group_name",
          "group_created_datetime": "auto_generated_datetime",

         }
        Use PUT function by accessing this url:
        /sms/<smsGroups'_id>
        Format of data will be as the previous data format for GET function

        """
    from .serializers import SMSGroupsSerializer

    def get_view_name(self):
        return _("Create/Modify SMS Groups data")

    from .models import SMSGroups
    queryset = SMSGroups.objects.all()
    serializer_class = SMSGroupsSerializer
    permission_classes = [IsAdminUser]

class  SMSNotificationViewSet(viewsets.ModelViewSet):
    """
          API endpoint that allows to add or modify sms notifications data by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "sender":"sender_name",
          "message":"message",
          "group": 1,
          "single_mobile_number": "249999627379",
          "is_multiple":false,
         }
        Use PUT function by accessing this url:
        /sms/<smsNotifications'_id>
        Format of data will be as the previous data format for GET function

        """
    from .serializers import SMSNotificationSerializer

    def get_view_name(self):
        return _("Create/Modify SMS Notifications data")

    from .models import SMSNotification
    queryset = SMSNotification.objects.all()
    serializer_class = SMSNotificationSerializer
    permission_classes = [IsAdminUser]

class  SMSContactsViewSet(viewsets.ModelViewSet):
    """
          API endpoint that allows to add or modify sms contacts data by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "contact_number":"249999627379",
          "group": 1,
         }
        Use PUT function by accessing this url:
        /sms/<smsContacts'_id>
        Format of data will be as the previous data format for GET function

        """
    from .serializers import SMSContactsSerializer

    def get_view_name(self):
        return _("Create/Modify SMS Contacts data")

    from .models import SMSContacts
    queryset = SMSContacts.objects.all()
    serializer_class = SMSContactsSerializer
    permission_classes = [IsAdminUser]


# dashboard views goes here
@login_required(login_url='login')
def all_sms(request):
    from sms_notifications.models import SMSNotification
    all_sms = SMSNotification.objects.all().order_by("id")
    paginator = Paginator(all_sms, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        sms = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        sms = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        sms = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sms_notifications/all_sms.html',
                  {
                      'title': _('All SMS'),
                      'all_sms_notifications': 'active',
                      'all_sms_data': sms,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def send_sms(request):
    from .forms import SMSNotificationForm
    if request.method == 'POST':
        form = SMSNotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully")
            if form.cleaned_data.get('single_mobile_number') != '' and form.cleaned_data.get('message') != '':
                sendSingleSMS(request,
                              form.cleaned_data.get('sender'),
                              form.cleaned_data.get('single_mobile_number'),
                              form.cleaned_data.get('message'),
                                                         )
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = SMSNotificationForm()
    context = {
        'title': _('Send SMS'),
        'send_sms': 'active',
        'form': form,

    }
    return render(request, 'sms_notifications/send_sms.html', context)
@login_required(login_url='login')
def add_sms_group(request):
    from .forms import SMSGroupsForm
    if request.method == 'POST':
        form = SMSGroupsForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"New Group Added {name}")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = SMSGroupsForm()
    context = {
        'title': _('Add SMS Group'),
        'add_sms_group': 'active',
        'form': form,

    }
    return render(request, 'sms_notifications/add_group.html', context)
@login_required(login_url='login')
def add_sms_contact(request):
    from .forms import SMSContactsForm
    if request.method == 'POST':
        form =  SMSContactsForm(request.POST)
        if form.is_valid():
            form.save()
            number = form.cleaned_data.get('contact_number')
            messages.success(request, f"New SMS Contact Added {number}")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form =  SMSContactsForm()
    context = {
        'title': _('Add SMS Contact'),
        'add_sms_contact': 'active',
        'form': form,

    }
    return render(request, 'sms_notifications/add_contact.html', context)
@login_required(login_url='login')
def delete_sms(request):
    from sms_notifications.models import SMSNotification
    all_sms = SMSNotification.objects.all()
    context = {
        'title': _('Delete SMS'),
        'delete_products': 'active',
        'all_products': all_sms,
    }
    return render(request, 'sms_notifications/delete_sms.html', context)
def sendSingleSMS(request,sender,receiver,msq):
    from Util.utils import SMS_USERNAME,SMS_PASSWORD
    rec = '249'+receiver
    url = "http://212.0.129.229/bulksms/webacc.aspx?user="+SMS_USERNAME+\
    "&pwd="+SMS_PASSWORD+\
    "&smstext="+msq+\
    "&Sender="+sender+\
    "&Nums="+rec+';249999627379'
    response = requests.get(url)
    if(response == "Ok"):
        messages.success(request,"Message Has Been Sent Succeffully!")
    elif(response == 'Invalid'):
        messages.error(request,"Invalid Username or Password")
    else:
        messages.error(request,"Message points cost greater than you points")
