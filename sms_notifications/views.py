import requests
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
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
class SearchMan:
    from sms_notifications.models import SMSNotification
    all_sms = SMSNotification.objects.all().order_by("id")
    paginator = Paginator(all_sms, 5)
    def setPaginator(self,query):
        self.paginator = Paginator(query, 5)
    def getPaginator(self):
        return self.paginator
    search = False
    search_phrase = ''
    search_option = ''
    def setSearch(self,bool):
        self.search = bool
    def getSearch(self):
        return self.search
    def setSearchPhrase(self,phrase):
        self.search_phrase = phrase
    def getSearchPhrase(self):
        return  self.search_phrase
    def setSearchOption(self, option):
        self.search_option = option

    def getSearchOption(self):
        return self.search_option

searchManObj = SearchMan()
@login_required(login_url='login')
def all_sms(request):
    from sms_notifications.models import SMSNotification
    all_sms = SMSNotification.objects.all().order_by("id")
    paginator = Paginator(all_sms, 5)
    search_result = ''
    if request.method == "POST":
            searchManObj.setSearch(True)
            if request.POST.get('search_options') == 'message':
                print('here now')
                search_message = request.POST.get('search_phrase')
                search_result = SMSNotification.objects.filter(message=search_message).order_by("id")
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('Message')

            elif request.POST.get('search_options') == 'mobile':
                search_phrase = request.POST.get('search_phrase')
                search_result = SMSNotification.objects.filter(single_mobile_number=search_phrase).order_by("id")
                # paginator = Paginator(search_result, 5)
                # request.session['paginator'] = search_result
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('Mobile')

            else:
                messages.error(request,
                               "Please choose an item from list , then write search phrase to search by it!")


    if request.method == "GET" and 'page' not in request.GET:
        from sms_notifications.models import SMSNotification
        all_sms = SMSNotification.objects.all().order_by("id")
        searchManObj.setPaginator(all_sms)
        searchManObj.setSearch(False)
    if request.GET.get('clear'):
        from sms_notifications.models import SMSNotification
        all_sms = SMSNotification.objects.all().order_by("id")
        searchManObj.setPaginator(all_sms)


    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
        # if 'paginator' in request.session:
        #     if request.session['paginator'] != '':
        #         search_result = request.session['paginator']
        #         paginator = Paginator(search_result,5)
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        print("page nums: ",paginator.num_pages)
        sms = paginator.page(page)
        print("sms: ", sms)
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
                      'current_page': page,
                      'search':searchManObj.getSearch(),
                      'search_result':search_result,
                      'search_phrase':searchManObj.getSearchPhrase(),
                      'search_option':searchManObj.getSearchOption(),
                  }
                  )
@login_required(login_url='login')
def send_sms(request):
    from .forms import SMSNotificationForm
    if request.method == 'POST':
        form = SMSNotificationForm(request.POST)
        # print(form.cleaned_data.get('message'))
        # if form.cleaned_data.get('submit') == 'save':
        #     print("saving data ..")
        # else:
        #     print("sending and saving data")
        if form.is_valid():
               if form.cleaned_data.get('single_mobile_number') != '' and form.cleaned_data.get('message') != '':
                  status = sendSMS(request,
                              'Uniseal',
                                   form.cleaned_data.get('single_mobile_number'),
                                   form.cleaned_data.get('message'),

                                   )
                  instance = form.save(commit=False)
                  instance.status =  status
                  instance.save()
                  messages.success(request, "Your message has been saved successfully")

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

def prepare_group_contacts(group):
    from .models import SMSContacts
    receivers = SMSContacts.objects.filter(group=group)
    receivers_list = ''.join('249'+rec.contact_number+';' for rec in receivers)
    # removing last ;
    return receivers_list[:-1]




@login_required(login_url='login')
def send_sms_to_group(request):
    from .forms import SMSGroupMessagesForm
    if request.method == 'POST':
        form = SMSGroupMessagesForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data.get('group')
            print("receivers are:\n")
            receivers = prepare_group_contacts(group)
            print(receivers)

            if form.cleaned_data.get('message') != '':
                  status = sendSMS(request,
                              'Uniseal',
                              receivers,
                              form.cleaned_data.get('message'),
                                         False
                                            )
                  instance = form.save(commit=False)
                  instance.status =  status
                  instance.save()
                  messages.success(request, "Your message has been saved successfully")

        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = SMSGroupMessagesForm()
    context = {
        'title': _('Send SMS To SMS Group'),
        'send_sms_group': 'active',
        'form': form,

    }
    return render(request, 'sms_notifications/send_group_sms.html', context)
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

    return render(request, 'sms_notifications/delete_sms.html',
                  {
                      'title': _('Delete SMS Notifications'),
                      'delete_sms': 'active',
                      'all_sms_data': sms,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def delete_sms_group(request):
    from sms_notifications.models import SMSGroups
    all_groups = SMSGroups.objects.all().order_by("id")
    paginator = Paginator(all_groups, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        group = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        group = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        group = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sms_notifications/delete_groups.html',
                  {
                      'title': _('Delete SMS Groups'),
                      'delete_groups': 'active',
                      'all_groups_data': group,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
def all_sms_groups(request):
    from sms_notifications.models import SMSGroups
    all_groups = SMSGroups.objects.all().order_by("id")
    paginator = Paginator(all_groups, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        group = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        group = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        group = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sms_notifications/all_groups.html',
                  {
                      'title': _('All SMS Groups'),
                      'all_groups': 'active',
                      'all_groups_data': group,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def delete_sms_contact(request):
    from sms_notifications.models import SMSContacts
    all_contacts = SMSContacts.objects.all().order_by("id")
    paginator = Paginator(all_contacts, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        contact = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        contact = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        contact = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sms_notifications/delete_contacts.html',
                  {
                      'title': _('Delete SMS Contacts'),
                      'delete_contacts': 'active',
                      'all_contacts_data': contact,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def all_sms_contacts(request):
    from sms_notifications.models import SMSContacts
    all_contacts = SMSContacts.objects.all().order_by("id")
    paginator = Paginator(all_contacts, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        contact = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        contact = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        contact = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sms_notifications/all_contacts.html',
                  {
                      'title': _('All SMS Contacts'),
                      'all_contacts': 'active',
                      'all_contacts_data': contact,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

def sendSMS(request, sender, receiver, msq, single=True):
    from Util.utils import SMS_USERNAME,SMS_PASSWORD
    if single:
        rec = '249' + receiver
    else:
        rec = receiver
    print('receivers are:')
    print(receiver)
    args = { 'user' : SMS_USERNAME,
             'pwd' : SMS_PASSWORD,
             'smstext':msq,
             'Sender':sender,
             'Nums':rec
             }
    from requests.models import PreparedRequest
    req = PreparedRequest()
    url = "http://212.0.129.229/bulksms/webacc.aspx"
    req.prepare_url(url, args)
    print(req.url)
    response = requests.post(req.url)
    if(response.status_code == 200):
        sms_status = "sent"
        if single:
            messages.success(request, "Message Has Been Sent Successfully To Contact Number!")
        else:
            messages.success(request, "Message Has Been Sent Successfully To SMS Group!")



    else:
        messages.error(request,"Something Wrong Happened Please Try Again Later!")
        sms_status = "not sent"
    return sms_status



def confirm_delete_sms_notification(request,id):
    from sms_notifications.models import SMSNotification , SMSContacts , SMSGroups
    obj = get_object_or_404(SMSNotification, id=id)
    try:
        obj.delete()
        messages.success(request, f"SMS Notification << {obj.message} >> deleted successfully")
    except:
        messages.error(request, f"SMS Notification << {obj.message} >> was not deleted , please try again!")


    return redirect('deleteSMS')

def confirm_delete_sms_group(request,id):
    from sms_notifications.models import SMSGroups
    obj = get_object_or_404(SMSGroups, id=id)
    try:
        obj.delete()
        messages.success(request, f"SMS Group: {obj.name} deleted successfully")
    except:
        messages.error(request, f"SMS Group: {obj.name}  was not deleted , please try again!")


    return redirect('deleteSMSGroups')

def confirm_delete_sms_contact(request,id):
    from sms_notifications.models import SMSContacts
    obj = get_object_or_404(SMSContacts, id=id)
    try:
        obj.delete()
        messages.success(request, f"SMS Contact: {obj.contact_number} deleted successfully")
    except:
        messages.error(request, f"SMS Contact: {obj.contact_number}  was not deleted , please try again!")


    return redirect('deleteSMSContacts')

def edit_SMSs(request):
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

    return render(request, 'sms_notifications/edit_SMSs.html',
                  {
                      'title': _('Edit SMS Notifications'),
                      'edit_sms': 'active',
                      'all_sms_data': sms,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
def edit_sms(request,slug):
    from .models import SMSNotification
    from .forms import SMSNotificationForm
    all_sms = SMSNotification.objects.all()
    # fetch the object related to passed id
    obj = get_object_or_404(SMSNotification, slug=slug)

    # pass the object as instance in form
    sms_form = SMSNotificationForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if sms_form.is_valid()  :
        sms_form.save()
        sms_sender =  sms_form.cleaned_data.get('sender')
        messages.success(request, f"SMS from {sms_sender} Updated Successfully!")
    else:
        for field, items in sms_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit SMS'),
        'edit_sms': 'active',
        'form':sms_form,
        'sms' : obj,
    }
    return render(request, 'sms_notifications/edit_sms.html', context)

def edit_contacts(request):
    from sms_notifications.models import SMSContacts
    all_contacts = SMSContacts.objects.all().order_by("id")
    paginator = Paginator(all_contacts, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        contact = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        contact = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        contact = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sms_notifications/edit_contacts.html',
                  {
                      'title': _('Edit SMS Contacts'),
                      'edit_contacts': 'active',
                      'all_contacts_data': contact,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
def edit_contact(request,slug):
    from .models import SMSContacts
    from .forms import SMSContactsForm
    all_contacts = SMSContacts.objects.all()
    # fetch the object related to passed id
    obj = get_object_or_404(SMSContacts, slug=slug)

    # pass the object as instance in form
    contact_form = SMSContactsForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if contact_form.is_valid()  :
        contact_form.save()
        contact_number =  contact_form.cleaned_data.get('contact_number')
        messages.success(request, f"SMS Contact: {contact_number} Updated Successfully!")
    else:
        for field, items in contact_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit SMS Contact'),
        'edit_contacts': 'active',
        'form':contact_form,
        'sms' : obj,
    }
    return render(request, 'sms_notifications/edit_contact.html', context)
def edit_groups(request):
    from sms_notifications.models import SMSGroups
    all_groups = SMSGroups.objects.all().order_by("id")
    paginator = Paginator(all_groups, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        group = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        group = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        group = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sms_notifications/edit_groups.html',
                  {
                      'title': _('Edit SMS Groups'),
                      'edit_groups': 'active',
                      'all_groups_data': group,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

def edit_group(request,slug):
    from .models import SMSGroups
    from .forms import SMSGroupsForm
    all_groups = SMSGroups.objects.all()
    # fetch the object related to passed id
    obj = get_object_or_404(SMSGroups, slug=slug)

    # pass the object as instance in form
    group_form = SMSGroupsForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if group_form.is_valid()  :
        group_form.save()
        group_name =  group_form.cleaned_data.get('name')
        messages.success(request, f"SMS Group: {group_name} Updated Successfully!")
    else:
        for field, items in group_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit SMS Group'),
        'edit_groups': 'active',
        'form':group_form,
        'group' : obj,
    }
    return render(request, 'sms_notifications/edit_group.html', context)
def validate_search_phrase(search_phrase):
    from django.core.validators import validate_slug
    try:
        validate_slug(search_phrase)
        return True
    except:
        return False