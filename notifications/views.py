from django.shortcuts import render
from Util.permissions import IsAnonymousUser, UnisealPermission
from django.template.defaultfilters import slugify

from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from Util.utils import EnablePartialUpdateMixin, rand_slug, SearchMan, createExelFile, ReportMan, delete_temp_folder, \
    check_phone_number
# Create your views here.

class registerTokenIds(viewsets.ModelViewSet):
    """
          API endpoint that allows to register token ids data by the application automatically
          this endpoint allows only GET,PUT,DELETE function
          permissions to this view is restricted as the following:
          - Only admin users can use GET,PUT,DELETE functions on this endpoint
          - Other types of users are not allowed to use this endpoint
          Data will be retrieved in the following format using GET function:
        {
        "id": 26,
        "token_id": "long_token",
        "os_type": "os_type",

    }
    Use PUT function by accessing this url:
    /notifications/registerTokenId/<token's_id>
    Format of data will be as the previous data format for GET function

    """
    from .serializers import TokensSerializer
    from .models import TokenIDs
    queryset = TokenIDs.objects.all()
    serializer_class = TokensSerializer


    def get_view_name(self):
        return _("Register/Modify Token Ids")
searchManObj = SearchMan("Notifications")
report_man = ReportMan()
@staff_member_required(login_url='login')
def all_notifications(request):
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

    return render(request, 'notifications/all_notifications.html',
                  {
                      'title': _('All Users'),
                      'all_notifications': 'active',
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
    from .forms import NotificationsForm
    if request.method == 'POST':
        form = NotificationsForm(request.POST)
        if form.is_valid():
            notification = form.save()
            notification.slug = slugify(rand_slug())
            notification.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f" Notification << {title} >> has been sent successfully!")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = NotificationsForm()

    context = {
        'title': _('Send Notifications'),
        'send_notifications': 'active',
        'form': form,

    }
    return render(request, 'notifications/send_notifications.html', context)