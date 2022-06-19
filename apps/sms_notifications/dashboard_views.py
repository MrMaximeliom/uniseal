import requests
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from Util.utils import delete_temp_folder, SearchMan
from apps.common_code.views import BaseListView
from apps.sms_notifications.models import SMSNotification


class SMSListView(BaseListView):
    def get(self, request, *args, **kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session:
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            instances = searchManObj.get_queryset()
            searchManObj.setPaginator(instances)
            searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = searchManObj.getPaginator()
            instances = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            instances = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            instances = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'object_list': instances,
            self.main_active_flag: 'active',
            self.active_flag: "active",
            'current_page': page,
            'title': self.title,
            'search': searchManObj.getSearch(),
            'search_result': search_result,
            'search_phrase': searchManObj.getSearchPhrase(),
            'search_option': searchManObj.getSearchOption(),
            'search_error': searchManObj.getSearchError(),
            'create_report_tip': CREATE_REPORT_TIP,
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'data_js': {
                "empty_search_phrase": EMPTY_SEARCH_PHRASE,
            }
        }
        return super().get(request)

    def post(self, request, *args, **kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST and 'createExcel' not in request.POST:
            searchManObj.setSearch(True)
            if request.POST.get('search_options') == 'message':
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

        if request.POST.get('clear') == 'clear':
            instances = searchManObj.get_queryset()
            searchManObj.setPaginator(instances)
            searchManObj.setSearch(False)

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))

        else:
            page = None
        try:
            paginator = searchManObj.getPaginator()
            instances = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            instances = paginator.page(1)
            page = 1

        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            instances = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'object_list': instances,
            self.main_active_flag: 'active',
            self.active_flag: "active",
            'current_page': page,
            'title': self.title,
            'search': searchManObj.getSearch(),
            'search_result': search_result,
            'search_phrase': searchManObj.getSearchPhrase(),
            'search_option': searchManObj.getSearchOption(),
            'search_error': searchManObj.getSearchError(),
            'create_report_tip': CREATE_REPORT_TIP,
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'data_js': {
                "empty_search_phrase": EMPTY_SEARCH_PHRASE,

            }
        }
        return super().get(request)

class SMSGroupsListView(BaseListView):
    def get(self, request, *args, **kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session:
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            instances = searchManObj.get_queryset()
            searchManObj.setPaginator(instances)
            searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = searchManObj.getPaginator()
            instances = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            instances = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            instances = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'object_list': instances,
            self.main_active_flag: 'active',
            self.active_flag: "active",
            'current_page': page,
            'title': self.title,
            'search': searchManObj.getSearch(),
            'search_result': search_result,
            'search_phrase': searchManObj.getSearchPhrase(),
            'search_option': searchManObj.getSearchOption(),
            'search_error': searchManObj.getSearchError(),
            'create_report_tip': CREATE_REPORT_TIP,
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'data_js': {
                "empty_search_phrase": EMPTY_SEARCH_PHRASE,
            }
        }
        return super().get(request)

    def post(self, request, *args, **kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST and 'createExcel' not in request.POST:
            searchManObj.setSearch(True)
            if request.POST.get('search_options') == 'message':
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

        if request.POST.get('clear') == 'clear':
            instances = searchManObj.get_queryset()
            searchManObj.setPaginator(instances)
            searchManObj.setSearch(False)

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))

        else:
            page = None
        try:
            paginator = searchManObj.getPaginator()
            instances = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            instances = paginator.page(1)
            page = 1

        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            instances = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'object_list': instances,
            self.main_active_flag: 'active',
            self.active_flag: "active",
            'current_page': page,
            'title': self.title,
            'search': searchManObj.getSearch(),
            'search_result': search_result,
            'search_phrase': searchManObj.getSearchPhrase(),
            'search_option': searchManObj.getSearchOption(),
            'search_error': searchManObj.getSearchError(),
            'create_report_tip': CREATE_REPORT_TIP,
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'data_js': {
                "empty_search_phrase": EMPTY_SEARCH_PHRASE,

            }
        }
        return super().get(request)

# ends here



@staff_member_required(login_url='login')
def all_sms(request):
    searchManObj = SearchMan("SMSNotification")
    from apps.sms_notifications.models import SMSNotification
    all_sms = SMSNotification.objects.all().order_by("id")
    paginator = Paginator(all_sms, 5)
    search_result = ''
    if request.method == "POST":
            searchManObj.setSearch(True)
            if request.POST.get('search_options') == 'message':
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
        from apps.sms_notifications.models import SMSNotification
        all_sms = SMSNotification.objects.all().order_by("id")
        searchManObj.setPaginator(all_sms)
        searchManObj.setSearch(False)
    if request.GET.get('clear'):
        from apps.sms_notifications.models import SMSNotification
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
                      'sms_notifications':'active',
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

@staff_member_required(login_url='login')
def send_sms(request):
    from .forms import SMSNotificationForm
    if request.method == 'POST':
        form = SMSNotificationForm(request.POST)
        if form.is_valid():
               if form.cleaned_data.get('single_mobile_number') != '' and form.cleaned_data.get('message') != '':
                  #  check if send only request or send and save request
                  if 'send'  in request.POST:
                      status = sendSMS(request,
                                       'Uniseal',
                                       form.cleaned_data.get('single_mobile_number'),
                                       form.cleaned_data.get('message'))

                      instance = form.save(commit=False)
                  # send and save
                  else:
                      status = sendSMS(request,
                                       'Uniseal',
                                       form.cleaned_data.get('single_mobile_number'),
                                       form.cleaned_data.get('message'))

                      instance = form.save(commit=False)
                      instance.status = status
                      instance.save()
                      messages.success(request, "Your message has been sent and saved successfully")



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
        'sms_notifications': 'active',

    }
    return render(request, 'sms_notifications/sms/send_sms.html', context)

def prepare_group_contacts(group):
    from .models import SMSContacts
    receivers = SMSContacts.objects.filter(group=group)
    receivers_list = ''.join('249'+rec.contact_number+';' for rec in receivers)
    # removing last ;
    return receivers_list[:-1]


@staff_member_required(login_url='login')
def send_sms_to_group(request):
    from .forms import SMSGroupMessagesForm
    if request.method == 'POST':
        form = SMSGroupMessagesForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data.get('group')
            receivers = prepare_group_contacts(group)
            if form.cleaned_data.get('message') != '':
                if 'send' in request.POST:
                    print("send only")
                    status = sendSMS(request,
                                     'Uniseal',
                                     receivers,
                                     form.cleaned_data.get('message'),
                                     False
                                     )
                    instance = form.save(commit=False)
                    messages.success(request, "Your message has been sent successfully")

                else:
                    status = sendSMS(request,
                                     'Uniseal',
                                     receivers,
                                     form.cleaned_data.get('message'),
                                     False
                                     )
                    instance = form.save(commit=False)
                    instance.status = status
                    instance.save()
                    messages.success(request, "Your message has been sent and saved successfully")



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
        'sms_notifications': 'active',

    }
    return render(request, 'sms_notifications/groups/send_group_sms.html', context)

@staff_member_required(login_url='login')
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



@staff_member_required(login_url='login')
def validate_search_phrase(search_phrase):
    from django.core.validators import validate_slug
    try:
        validate_slug(search_phrase)
        return True
    except:
        return False
