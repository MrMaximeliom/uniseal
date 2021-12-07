from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from pyfcm import FCMNotification

from Util.utils import rand_slug, SearchMan, ReportMan, delete_temp_folder

# Create your views here.
def testNotifs():
    from pyapns_client import APNSClient, IOSPayloadAlert, IOSPayload, IOSNotification, APNSDeviceException, \
        APNSServerException, APNSProgrammingException, UnregisteredException

    client = APNSClient(mode=APNSClient.MODE_DEV, root_cert_path='apns-dev-cer.pem', auth_key_path='AuthKey_AN96P2J2W5.p8',
                        auth_key_id='AN96P2J2W5', team_id='APN1234567')
    # `root_cert_path` is for the AAACertificateServices root cert (https://apple.co/3mZ5rB6)
    # with token-based auth you don't need to create / renew your APNS SSL certificates anymore
    # you can pass `None` to `root_cert_path` if you have the cert included in your trust store
    # httpx uses 'SSL_CERT_FILE' and 'SSL_CERT_DIR' from `os.environ` to find your trust store

    try:
        from notifications.models import TokenIDs

        device_tokens = TokenIDs.objects.filter(os_type="ios")
        alert = IOSPayloadAlert(title='Title', subtitle='Subtitle', body='Hello How are you?')
        payload = IOSPayload(alert=alert)
        notification = IOSNotification(payload=payload, topic='com.unigroup.uniseal')

        for device_token in device_tokens:
            try:
                client.push(notification=notification, device_token=device_token)
            except UnregisteredException as e:
                print(f'device is unregistered, compare timestamp {e.timestamp_datetime} and remove from db')
            except APNSDeviceException:
                print('flag the device as potentially invalid and remove from db after a few tries')
            except APNSServerException:
                print('try again later')
            except APNSProgrammingException:
                print('check your code and try again later')
            else:
                print('everything is ok')
    finally:
        client.close()

searchManObj = SearchMan("Notifications")
report_man = ReportMan()
@staff_member_required(login_url='login')
def all_notifications(request):
    testNotifs()
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
    NOTIFICATION_TITLE_SYNTAX_ERROR,
    NOTIFICATION_BODY_SYNTAX_ERROR,
    NOTIFICATION_NOT_FOUND,
    )
    from .models import Notifications
    all_notifications = Notifications.objects.all().order_by("id")
    paginator = Paginator(all_notifications, 60)

    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    # create search functionality
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'title':
            print('here now')
            search_message = request.POST.get('search_phrase')
            search_result = Notifications.objects.filter(title__icontains=search_message).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Notification Title')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'body':
            search_phrase = request.POST.get('search_phrase')
            search_result = Notifications.objects.filter(body__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Notification Body')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'os_type':
            search_phrase = request.POST.get('search_phrase')
            search_result = Notifications.objects.filter(token_id__os_type__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('OS Type')
            searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_notifications = Notifications.objects.all().order_by("id")
        searchManObj.setPaginator(all_notifications)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_notifications = Notifications.objects.all().order_by("id")
        searchManObj.setPaginator(all_notifications)
        searchManObj.setSearch(False)
    # create report functionality

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = 1

    try:
        paginator = searchManObj.getPaginator()
        print("paginator is: ",paginator)
        notifications = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        notifications = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        notifications = paginator.page(paginator.num_pages)
        page = paginator.num_pagespaginator.page_range,
    print(paginator.page_range)


    return render(request, 'notifications/all_notifications.html',
                  {
                      'title': _('All Notifications'),
                      'all_notifications': 'active',
                      'notifications':'active',
                      'all_notifications_data': notifications,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "title_error": NOTIFICATION_TITLE_SYNTAX_ERROR,
                          "body_error": NOTIFICATION_BODY_SYNTAX_ERROR,
                          "not_found": NOTIFICATION_NOT_FOUND
                      }
                  }
                  )
@staff_member_required(login_url='login')
def send_notifications(request):
    from .models import TokenIDs
    if request.method == 'POST':

        # form.token_id = TokenIDs.objects.all()[0]
       if request.POST.get('title') != '' and request.POST.get('body') != ''  and request.POST.get('os-options') != '':
            proxy_dict = {
                "http": "http://93.188.162.130:9000",

            }

            server_key = 'AAAAEpL69vw:APA91bHRu0kEXCHqZ22U9SnrNr9VSYpvjyEo4o2kx07Tdeo5XL1UJZrmk0mWSbiA6PoNgbqJZaWSnOMkCXZxLTC6dRAtAFcDtB7f3sYyCHqZ7n_i12oThUboFstOvj5yWiPB5X1_L3uh'
            message_title = request.POST.get('title')
            message_body = request.POST.get('body')
            os_type = request.POST.get('os-options')
            if os_type == 'android':
                android_tokens = TokenIDs.objects.all().filter(os_type="android")
                android_tokens_list = list()
                for token in android_tokens:
                    android_tokens_list.append(token.reg_id)
                FCMNotification(api_key=server_key,proxy_dict=proxy_dict).notify_multiple_devices(registration_ids=android_tokens_list,message_title=message_title,
                 message_body=message_body,data_message={'type':'notification'},click_action='FLUTTER_NOTIFICATION_CLICK')
            elif os_type == 'ios':
                ios_tokens = TokenIDs.objects.all().filter(os_type="ios")
                ios_tokens_list = list()
                for token in  ios_tokens:
                    ios_tokens_list.append(token.reg_id)
                FCMNotification(api_key=server_key,proxy_dict=proxy_dict).notify_multiple_devices(
                    registration_ids=ios_tokens_list, message_title=message_title,
                    message_body=message_body,data_message={'type':'notification'},click_action='FLUTTER_NOTIFICATION_CLICK')

            else:
                all_tokens = TokenIDs.objects.all()
                all_tokens_list = list()
                for token in all_tokens:
                    all_tokens_list.append(token.reg_id)
                FCMNotification(api_key=server_key,proxy_dict=proxy_dict).notify_multiple_devices(
                    registration_ids=all_tokens_list, message_title=message_title,
                    message_body=message_body,data_message={'type':'notification'},click_action='FLUTTER_NOTIFICATION_CLICK')

            from notifications.models import TokenIDs
            reg_id = get_object_or_404(TokenIDs,id=58)
            # objs = Entry.objects.bulk_create([
            #     ...     Entry(headline='This is a test'),
            #     ...     Entry(headline='This is only a test'),
            #     ...])
            all_tokens = TokenIDs.objects.all()
            from .models import Notifications
            list_notifications = list()
            for token in all_tokens:
                list_notifications.append(
                    Notifications(
                        token_id=token,
                        title=message_title,
                        body=message_body,
                        slug=slugify(rand_slug())
                    )
                )
            objects = Notifications.objects.bulk_create(list_notifications)

            messages.success(request, f" Notification << {message_title} >> has been sent successfully!")

       else:
                    messages.error(request,"There was an error please try again later!")


    context = {
        'title': _('Send Notifications'),
        'send_notifications': 'active',
        'notifications': 'active',


    }
    return render(request, 'notifications/send_notifications.html', context)
@staff_member_required(login_url='login')
def delete_notifications(request):
    from .models import Notifications
    all_notifications = Notifications.objects.all().order_by("id")
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        NOTIFICATION_TITLE_SYNTAX_ERROR,
        NOTIFICATION_BODY_SYNTAX_ERROR,
        NOTIFICATION_NOT_FOUND,
    )
    paginator = Paginator(all_notifications, 5)

    search_result = ''

    # create search functionality
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'title':
            print('here now')
            search_message = request.POST.get('search_phrase')
            search_result = Notifications.objects.filter(title__icontains=search_message).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Notification Title')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'body':
            search_phrase = request.POST.get('search_phrase')
            search_result = Notifications.objects.filter(body__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Notification Body')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'os_type':
            search_phrase = request.POST.get('search_phrase')
            search_result = Notifications.objects.filter(token_id__os_type__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('OS Type')
            searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_notifications = Notifications.objects.all().order_by("id")
        searchManObj.setPaginator(all_notifications)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_notifications = Notifications.objects.all().order_by("id")
        searchManObj.setPaginator(all_notifications)
        searchManObj.setSearch(False)
    # create report functionality

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        notifications = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        notifications = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        notifications = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'notifications/delete_notifications.html',
                  {
                      'title': _('Delete Notifications'),
                      'delete_notifications': 'active',
                      'notifications': 'active',
                      'all_notifications': all_notifications,
                      'all_notifications_data': notifications,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "title_error": NOTIFICATION_TITLE_SYNTAX_ERROR,
                          "body_error": NOTIFICATION_BODY_SYNTAX_ERROR,
                          "not_found": NOTIFICATION_NOT_FOUND,

                      }
                  }
                  )


def confirm_delete(request, id, url):
    from .models import Notifications
    obj = get_object_or_404(Notifications, id=id)
    try:
        obj.delete()
        messages.success(request, f"Notification << {obj.title} >> deleted successfully")
    except:
        messages.error(request, f"Notification << {obj.title} >> was not deleted , please try again!")

    return redirect(url)
@staff_member_required(login_url='login')
def edit_notifications(request):
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
    NOTIFICATION_TITLE_SYNTAX_ERROR,
    NOTIFICATION_BODY_SYNTAX_ERROR,
    NOTIFICATION_NOT_FOUND,
    )
    from .models import Notifications
    all_notifications = Notifications.objects.all().order_by("id")
    paginator = Paginator(all_notifications, 5)

    search_result = ''
    # create search functionality
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'title':
            print('here now')
            search_message = request.POST.get('search_phrase')
            search_result = Notifications.objects.filter(title__icontains=search_message).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Notification Title')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'body':
            search_phrase = request.POST.get('search_phrase')
            search_result = Notifications.objects.filter(body__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Notification Body')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'os_type':
            search_phrase = request.POST.get('search_phrase')
            search_result = Notifications.objects.filter(token_id__os_type__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('OS Type')
            searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_notifications = Notifications.objects.all().order_by("id")
        searchManObj.setPaginator(all_notifications)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_notifications = Notifications.objects.all().order_by("id")
        searchManObj.setPaginator(all_notifications)
        searchManObj.setSearch(False)
    # create report functionality

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        notifications = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        notifications = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        notifications = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'notifications/resend_notifications.html',
                  {
                      'title': _('Resend Notifications'),
                      'resend_notifications': 'active',
                      'notifications': 'active',
                      'all_notifications_data': notifications,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "title_error": NOTIFICATION_TITLE_SYNTAX_ERROR,
                          "body_error": NOTIFICATION_BODY_SYNTAX_ERROR,
                          "not_found": NOTIFICATION_NOT_FOUND
                      }
                  }
                  )