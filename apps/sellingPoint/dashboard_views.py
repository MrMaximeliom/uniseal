from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder
from apps.sellingPoint.models import SellingPoint
from apps.common_code.views import BaseListView

from Util.utils import (get_selected_pages,prepare_selected_query,prepare_default_query,get_fields_names_for_report_file)


sellingPoints = SellingPoint.objects.all().order_by("id")
searchManObj = SearchMan("Selling Point")
report_man = ReportMan()
# new code starts here
class SellingPointsListView(BaseListView):
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
            if request.POST.get('search_options') == 'selling_point_name':
                search_message = request.POST.get('search_phrase')
                search_result = SellingPoint.objects.filter(name=search_message).order_by('id')
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('Selling Point Name')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'country':
                search_phrase = request.POST.get('search_phrase')
                search_result = SellingPoint.objects.filter(country__name=search_phrase).order_by("id")
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('Country')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'state':
                search_phrase = request.POST.get('search_phrase')
                search_result = SellingPoint.objects.filter(state__name=search_phrase).order_by("id")
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('State')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'city':
                search_phrase = request.POST.get('search_phrase')
                search_result = SellingPoint.objects.filter(city__name=search_phrase).order_by("id")
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('City')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'area':
                search_phrase = request.POST.get('search_phrase')
                print('search phrase is ', search_phrase)
                search_result = SellingPoint.objects.filter(area__name=search_phrase).order_by("id")
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('Area')
                searchManObj.setSearchError(False)
            else:
                messages.error(request,
                               "Please choose an item from list , then write search phrase to search by it!")
                searchManObj.setSearchError(True)

        if request.method == "POST" and request.POST.get('createExcel') == 'done':
            headers = []
            headers.append("name") if request.POST.get('point_header') is not None else ''
            headers.append("country") if request.POST.get('country_header') is not None else ''
            headers.append("state") if request.POST.get('state_header') is not None else ''
            headers.append("city") if request.POST.get('city_header') is not None else ''
            headers.append("area") if request.POST.get('area_header') is not None else ''
            headers.append("phone_number") if request.POST.get('primary_phone_header') is not None else ''
            headers.append("secondary_phone") if request.POST.get('secondary_phone_header') is not None else ''
            headers.append("email") if request.POST.get('email_header') is not None else ''
            # create report functionality
            # setting all data as default behaviour
            if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
                # get requested pages from the paginator of original page
                selected_pages = get_selected_pages(request.POST.get('pages_collector'))
                query = searchManObj.getPaginator()
                if len(headers) > 0:
                    print(headers)
                    constructor= prepare_selected_query(searchManObj.get_queryset(),headers,selected_pages,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Selling_Points',
                                                                                      headers, **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


                else:
                    headers = get_fields_names_for_report_file(SellingPoint,SellingPoint.get_not_wanted_fields_names_in_report_file())
                    print(headers)
                    constructor = prepare_selected_query(searchManObj.get_queryset(),headers,selected_pages,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Selling_Points',
                                                                                      headers,
                                                                                      **constructor
                                                                                      )
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
                # get the original query of page and then structure the data
            else:
                query = searchManObj.getPaginator()
                if len(headers) > 0:
                    print(headers)
                    constructor = prepare_default_query(searchManObj.get_queryset(),headers,query)

                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Selling_Points',
                                                                                      headers, **constructor)
                    if status:

                        messages.success(request, f"Report Successfully Created ")
                        request.session['temp_dir'] = 'delete man!'
                        # return redirect('download_file',filepath=filepath,filename=filename)

                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

                else:
                    print(headers)
                    headers = get_fields_names_for_report_file(SellingPoint,SellingPoint.get_not_wanted_fields_names_in_report_file())
                    constructor = prepare_default_query(searchManObj.get_queryset(),headers,query)
                    status, filePath, fileName = createExelFile('Report_For_Selling_Points',
                                                                headers,
                                                                **constructor
                                                                )
                    report_man.setFileName(fileName)
                    report_man.setFilePath(filePath)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created")
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

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



@staff_member_required(login_url='login')
def selling_point_details(request,slug):
    from .models import SellingPoint
    point = get_object_or_404(SellingPoint, slug=slug)


    return render(request, 'sellingPoints/selling_point_detail.html',
                  {
                      'title': _('Selling Point Details'),
                      'all_products': 'active',
                      'selling_points': 'active',
                      'point_data': point,
                  }
                  )
