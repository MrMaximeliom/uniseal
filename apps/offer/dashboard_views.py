from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from Util.search_form_strings import CLEAR_SEARCH_TIP,\
    SEARCH_JOB_TYPE_TIP ,\
    OFFER_NOT_FOUND, ALL_OFFERS_TITLE,\
    EDIT_OFFERS_TITLE , ADD_OFFERS_TITLE
from Util.utils import delete_temp_folder, SearchMan, ReportMan
from .models import Offer
from .forms import OfferForm
from django.views.generic.edit import FormView
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import UpdateView


class OfferFormView(FormView):
    template_name = 'offer/add_offers.html'
    form_class = OfferForm
    success_url = 'addOffers'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Offer Added Successfully")
        return super().form_valid(form)

    extra_context = {
        'offer': 'active',
        'add_offers': 'active',
        'title':ADD_OFFERS_TITLE
    }


class OffersListView(ListView):
    model = Offer
    template_name = "offer/all_offers.html"
    active_flag = 'all_offers'
    searchManObj = SearchMan("Offer")
    search_result = None
    report_man = ReportMan()
    title = ALL_OFFERS_TITLE




    def get_queryset(self):
        return Offer.objects.all().order_by('-id')

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            self.search_result = Offer.objects.all().filter(
                name=search_message).order_by('-num_users')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Offer Start Date')
            self.searchManObj.setSearchError(False)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.POST.get('clear') == 'clear':
            job_types = self.get_queryset()
            self.searchManObj.setPaginator(job_types)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            job_types = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            job_types = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            job_types = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'job': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'object_list': job_types,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_job_type_tip': SEARCH_JOB_TYPE_TIP,
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
            job_types = Offer.objects.all().order_by('-id')
            self.searchManObj.setPaginator(job_types)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            job_types = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            job_types = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            job_types = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'job': 'active',
            self.active_flag: 'active',

            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'object_list': job_types,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_job_types_tip': SEARCH_JOB_TYPE_TIP,
            'not_found':JOB_TYPE_NOT_FOUND,
            'current_page': page,
            'title': self.title
        }
        return super().get(request)


class JopTypeUpdateView(UpdateView):
    model = JopType
    success_url = reverse_lazy('editJobTypes')
    template_name = "job_type/edit_job_type.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Job Type Updated Successfully")
        return super().form_valid(form)
    fields = ['name']
    extra_context = {
        'job': 'active',
        'edit_job_types': 'active',
        'title':EDIT_JOB_TYPE_TITLE

    }


def confirm_delete(request, slug):
    from .models import JopType
    obj = get_object_or_404(JopType, slug=slug)
    try:
        obj.delete()
        messages.success(request, f"JopType {obj.name} deleted successfully")
    except:
        messages.error(request, f"JopType {obj.name} was not deleted , please try again!")
    return redirect('deleteJobTypes')
