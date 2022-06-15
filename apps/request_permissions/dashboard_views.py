from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from Util.search_form_strings import CLEAR_SEARCH_TIP, \
    SEARCH_JOB_TYPE_TIP, SEARCH_REQUESTS_TIP, REQUEST_ACCESS_TITLE, PERMISSION_NOT_FOUND
from Util.utils import delete_temp_folder, SearchMan, ReportMan
from .models import RequestAccess


def GiveOrDenyAccess(request,pk):
    from apps.request_permissions.models import RequestAccess
    request_access = get_object_or_404(RequestAccess,pk=pk)
    if request_access:
        if not request_access.status:
            request_access.status=True
            request_access.save()
            messages.success(request,f"User {request_access.user.full_name} has a permission to view Approvals Page")
        else:
            request_access.status=False
            request_access.save()
            messages.success(request, f"User {request_access.user.full_name} has no permission to view Approvals Page")


    else:
        messages.error(request,f"Sorry Try Again Later")
    return redirect('requestAccessList')



class RequestAccessListView(ListView):
    model = RequestAccess
    template_name = "request_permissions/all_requests.html"
    active_flag = 'request'
    searchManObj = SearchMan("Request")
    search_result = None
    report_man = ReportMan()
    title = REQUEST_ACCESS_TITLE

    def get_queryset(self):
        return RequestAccess.objects.annotate(num_users=Count('user')).order_by('-num_users')

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if request.POST.get('search_phrase') != '' and request.POST.get('search_options') == 'full_name':
            search_message = request.POST.get('search_phrase')
            self.search_result = RequestAccess.objects.annotate(num_users=Count('user')).filter(
                user__full_name=search_message).order_by('-num_users')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Full Name')
            self.searchManObj.setSearchError(False)
        if request.POST.get('search_phrase') != '' and request.POST.get('search_options') == 'username':
            search_message = request.POST.get('search_phrase')
            self.search_result = RequestAccess.objects.annotate(num_users=Count('user')).filter(
                user__username=search_message).order_by('-num_users')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Username')
            self.searchManObj.setSearchError(False)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.POST.get('clear') == 'clear':
            requests_list = self.get_queryset()
            self.searchManObj.setPaginator(requests_list)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            requests_list = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            requests_list = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            requests_list = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'job': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'requests_list': requests_list,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_requests_tip': SEARCH_JOB_TYPE_TIP,
            'current_page': page,
            'title':self.title
        }
        return super().get(request)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session:
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            requests = RequestAccess.objects.annotate(num_users=Count('user')).order_by('-num_users')
            self.searchManObj.setPaginator(requests)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            requests = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            requests = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            requests = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'requests': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'requests_list': requests,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_request_tip': SEARCH_REQUESTS_TIP ,
            'not_found':PERMISSION_NOT_FOUND,
            'current_page': page,
            'title': self.title
        }
        return super().get(request)

