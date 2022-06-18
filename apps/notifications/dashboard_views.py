from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from pyfcm import FCMNotification

from Util.utils import rand_slug, SearchMan, ReportMan, delete_temp_folder

# Create your views here.
# NEW CODE
from apps.common_code.views import BaseListView
from .models import Notifications


class NotificationListView(BaseListView):
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
            if request.POST.get('search_options') == 'title':
                print('here now')
                search_message = request.POST.get('search_phrase')
                search_result = Notifications.objects.filter(title__icontains=search_message).order_by("id")
                searchManObj.setPaginator(search_result, 60)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('Notification Title')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'body':
                search_phrase = request.POST.get('search_phrase')
                search_result = Notifications.objects.filter(body__icontains=search_phrase).order_by("id")
                searchManObj.setPaginator(search_result, 60)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('Notification Body')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'os_type':
                search_phrase = request.POST.get('search_phrase')
                search_result = Notifications.objects.filter(token_id__os_type__icontains=search_phrase).order_by("id")
                searchManObj.setPaginator(search_result, 60)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('OS Type')
                searchManObj.setSearchError(False)
            else:
                messages.error(request,
                               "Please choose an item from list , then write search phrase to search by it!")
                searchManObj.setSearchError(True)

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



# END NEW CODE

searchManObj = SearchMan("Notifications")
report_man = ReportMan()




@staff_member_required(login_url='login')
def send_notifications(request):
    if request.method == 'POST':

        # form.token_id = TokenIDs.objects.all()[0]
        from apps.notifications.models import TokenIDs
        all_tokens = TokenIDs.objects.all()
        if all_tokens.exists():
            if request.POST.get('title') != '' and request.POST.get('body') != '' and request.POST.get(
                    'os-options') != '':
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
                    FCMNotification(api_key=server_key, proxy_dict=proxy_dict).notify_multiple_devices(
                        registration_ids=android_tokens_list, message_title=message_title,
                        message_body=message_body, data_message={'type': 'notification'},
                        click_action='FLUTTER_NOTIFICATION_CLICK')
                elif os_type == 'ios':
                    ios_tokens = TokenIDs.objects.all().filter(os_type="ios")
                    ios_tokens_list = list()
                    for token in ios_tokens:
                        ios_tokens_list.append(token.reg_id)
                    FCMNotification(api_key=server_key, proxy_dict=proxy_dict).notify_multiple_devices(
                        registration_ids=ios_tokens_list, message_title=message_title,
                        message_body=message_body, data_message={'type': 'notification'},
                        click_action='FLUTTER_NOTIFICATION_CLICK')

                else:
                    all_tokens = TokenIDs.objects.all()
                    all_tokens_list = list()
                    for token in all_tokens:
                        all_tokens_list.append(token.reg_id)
                    FCMNotification(api_key=server_key, proxy_dict=proxy_dict).notify_multiple_devices(
                        registration_ids=all_tokens_list, message_title=message_title,
                        message_body=message_body, data_message={'type': 'notification'},
                        click_action='FLUTTER_NOTIFICATION_CLICK')

                from .models import Notifications
                list_notifications = list()
                print("here now dood")
                print(all_tokens)
                for token in all_tokens:
                    print(token)
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
            messages.error(request, "Please add device tokens first!")

    context = {
        'title': _('Send Notifications'),
        'send_notifications': 'active',
        'notifications': 'active',

    }
    return render(request, 'notifications/send_notifications.html', context)





