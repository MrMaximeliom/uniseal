from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from Util.search_form_strings import CLEAR_SEARCH_TIP,\
    SEARCH_OFFERS_TIP ,\
    OFFER_NOT_FOUND, ALL_OFFERS_TITLE,\
    EDIT_OFFERS_TITLE , ADD_OFFERS_TITLE
from Util.utils import delete_temp_folder, SearchMan, ReportMan
from .models import Offer
from .forms import OfferForm
from django.views.generic.edit import FormView
from django.contrib import messages
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
        'offers': 'active',
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
        if request.POST.get('search_phrase') != '' and request.POST.get('search_options') == 'start_date':
            search_message = request.POST.get('search_phrase')
            self.search_result = Offer.objects.all().filter(
                name=search_message).order_by('-id')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Offer Start Date')
            self.searchManObj.setSearchError(False)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.POST.get('clear') == 'clear':
            offers = self.get_queryset()
            self.searchManObj.setPaginator(offers)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            offers = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            offers = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            offers = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'offers': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'offers_list': offers,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_offers_tip': SEARCH_OFFERS_TIP,
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
            offers = Offer.objects.all().order_by('-id')
            self.searchManObj.setPaginator(offers)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            offers = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            offers = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            offers = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'offers': 'active',
            self.active_flag: 'active',

            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'offers_list': offers,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_offers_tip': SEARCH_OFFERS_TIP,
            'not_found':OFFER_NOT_FOUND,
            'current_page': page,
            'title': self.title
        }
        return super().get(request)


class OfferUpdateView(UpdateView):
    model = Offer
    success_url = reverse_lazy('editOffer')
    template_name = "offer/edit_offer.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Offer Updated Successfully")
        return super().form_valid(form)
    fields = "__all__"
    extra_context = {
        'job': 'active',
        'edit_offers': 'active',
        'title':EDIT_OFFERS_TITLE,
        'clear_search_tip': CLEAR_SEARCH_TIP,
        'search_offers_tip': SEARCH_OFFERS_TIP,

    }


def confirm_delete(request, slug):
    from .models import Offer
    obj = get_object_or_404(Offer, slug=slug)
    try:
        obj.delete()
        messages.success(request, f"Offer {obj.name} deleted successfully")
    except:
        messages.error(request, f"Offer {obj.name} was not deleted , please try again!")
    return redirect('deleteOffers')
