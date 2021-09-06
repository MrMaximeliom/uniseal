from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from Util.utils import rand_slug
from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder
from django.contrib.admin.views.decorators import staff_member_required

from address.models import Area
areas = Area.objects.annotate(num=Count('city')).order_by('-num')

def prepare_selected_query_city(selected_pages, paginator_obj, headers=None):
    area_list = []
    city_list = []
    headers_here = ["Area","City"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Area":
                for page in selected_pages:
                    for area in paginator_obj.page(page):
                        area_list.append(area.name)
            elif header == "City":
                for page in selected_pages:
                    for area in paginator_obj.page(page):
                        city_list.append(area.city.name)


    else:
        for page in range(1, paginator_obj.num_pages + 1):
            for area in paginator_obj.page(page):
                area_list.append(area.name)
                city_list.append(area.city.name)

    return headers_here, city_list,area_list


def prepare_query_city(paginator_obj, headers=None):
    areas = []
    cities = []
    headers_here = ["Area","City"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "City":
                for page in range(1, paginator_obj.num_pages + 1):
                    for area in paginator_obj.page(page):
                        cities.append(area.city.name)
            elif header == "Area":
                for page in range(1, paginator_obj.num_pages + 1):
                    for area in paginator_obj.page(page):
                        areas.append(area.name)

    else:
        for page in range(1, paginator_obj.num_pages + 1):
            for area in paginator_obj.page(page):
                areas.append(area.name)
                cities.append(area.city.name)

    return headers_here, cities,areas
search_man_areas = SearchMan("Area")
report_man_areas = ReportMan()
@staff_member_required(login_url='login')
def all_areas(request):
    paginator = Paginator(areas, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        CITY_NAME_SYNTAX_ERROR,
        AREA_NAME_SYNTAX_ERROR

    )
    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        search_man_areas.setSearch(True)
        if request.POST.get('search_options') == 'city':
            search_message = request.POST.get('search_phrase')
            search_result = Area.objects.filter(
                city__name__icontains=search_message).order_by('id')
            search_man_areas.setPaginator(search_result)
            search_man_areas.setSearchPhrase(search_message)
            search_man_areas.setSearchOption('City')
            search_man_areas.setSearchError(False)

        elif request.POST.get('search_options') == 'area':
            search_message = request.POST.get('search_phrase')
            search_result = Area.objects.filter(
                name__icontains=search_message).order_by('id')
            search_man_areas.setPaginator(search_result)
            search_man_areas.setSearchPhrase(search_message)
            search_man_areas.setSearchOption('Area')
            search_man_areas.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter city name first!")
            search_man_areas.setSearchError(True)

    if request.method == "GET" and 'page' not in request.GET and not search_man_areas.getSearch():
        all_areas = Area.objects.all().order_by('id')
        search_man_areas.setPaginator(all_areas)
        search_man_areas.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_areas = Area.objects.filter().order_by('id')
        search_man_areas.setPaginator(all_areas)
        search_man_areas.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("City")
        headers.append("Area")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = search_man_areas.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers,  cities_list, areas_list = prepare_selected_query_city(
                    selected_pages=selected_pages,
                    paginator_obj=query,
                    headers=headers)
                if len(cities_list) > 0:
                    constructor.update({"city": cities_list})
                if len(areas_list) > 0:
                    constructor.update({"area": areas_list})
                status, report_man_areas.filePath, report_man_areas.fileName = createExelFile('Report_For_Areas',
                                                                                              headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man_areas.filePath), str(report_man_areas.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers,  cities_list, areas_list = prepare_selected_query_city(
                    selected_pages, query, headers)
                status, report_man_areas.filePath, report_man_areas.fileName = createExelFile('Report_For_Areas',
                                                                                              headers,

                                                                                              city=cities_list,
                                                                                              area=areas_list
                                                                                              )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_areas.filePath), str(report_man_areas.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            print("pages collector is none")
            query = search_man_areas.getPaginator()
            print("query in major if is: ", query.num_pages)
            if len(headers) > 0:
                print("in major if")
                constructor = {}
                headers,  cities_list, areas_list = prepare_query_city(query, headers=headers)
                if len(cities_list) > 0:
                    constructor.update({"city": cities_list})
                if len(areas_list) > 0:
                    constructor.update({"area": areas_list})

                status, report_man_areas.filePath, report_man_areas.fileName = createExelFile('Report_For_Areas',
                                                                                              headers, **constructor)
                if status:

                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_areas.filePath), str(report_man_areas.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers,  cities_list, areas_list = prepare_query_city(query)
                status, report_man_areas.filePath, report_man_areas.fileName = createExelFile('Report_For_Areas',
                                                                                              headers,

                                                                                              city=cities_list,
                                                                                              area=areas_list
                                                                                              )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man_areas.filePath), str(report_man_areas.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = search_man_areas.getPaginator()
        areas_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        areas_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        areas_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/all_areas.html',
                  {
                      'title': _('All Areas'),
                      'all_areas': 'active',
                      'all_areas_data': areas_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': search_man_areas.getSearch(),
                      'search_result': search_result,
                      'search_phrase': search_man_areas.getSearchPhrase(),
                      'search_option': search_man_areas.getSearchOption(),
                      'search_error': search_man_areas.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "city_error": CITY_NAME_SYNTAX_ERROR,
                          "area_error": AREA_NAME_SYNTAX_ERROR
                      }
                  }
                  )


@staff_member_required(login_url='login')
def add_areas(request):
    from .forms import AreaForm
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            area = form.save()
            area.slug = slugify(rand_slug())
            area.save()
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"New Area Added: {name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = AreaForm()
    context = {
        'title': _('Add Areas'),
        'add_areas': 'active',
        'form': form
    }

    return render(request, 'address/add_areas.html', context)


@staff_member_required(login_url='login')
def delete_areas(request):
    paginator = Paginator(areas, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        CITY_NAME_SYNTAX_ERROR,
        AREA_NAME_SYNTAX_ERROR

    )
    search_result = ''
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        search_man_areas.setSearch(True)
        if request.POST.get('search_options') == 'city':
            search_message = request.POST.get('search_phrase')
            search_result = Area.objects.filter(
                city__name__icontains=search_message).order_by('id')
            search_man_areas.setPaginator(search_result)
            search_man_areas.setSearchPhrase(search_message)
            search_man_areas.setSearchOption('City')
            search_man_areas.setSearchError(False)

        elif request.POST.get('search_options') == 'area':
            search_message = request.POST.get('search_phrase')
            search_result = Area.objects.filter(
                name__icontains=search_message).order_by('id')
            search_man_areas.setPaginator(search_result)
            search_man_areas.setSearchPhrase(search_message)
            search_man_areas.setSearchOption('Area')
            search_man_areas.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter city name first!")
            search_man_areas.setSearchError(True)

    if request.method == "GET" and 'page' not in request.GET and not search_man_areas.getSearch():
        all_areas = Area.objects.all().order_by('id')
        search_man_areas.setPaginator(all_areas)
        search_man_areas.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_areas = Area.objects.filter().order_by('id')
        search_man_areas.setPaginator(all_areas)
        search_man_areas.setSearch(False)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = search_man_areas.getPaginator()
        areas_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        areas_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        areas_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/delete_areas.html',
                  {
                      'title': _('Delete Areas'),
                      'delete_areas': 'active',
                      'all_areas_data': areas_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': search_man_areas.getSearch(),
                      'search_result': search_result,
                      'search_phrase': search_man_areas.getSearchPhrase(),
                      'search_option': search_man_areas.getSearchOption(),
                      'search_error': search_man_areas.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "city_error": CITY_NAME_SYNTAX_ERROR,
                          "area_error": AREA_NAME_SYNTAX_ERROR
                      }
                  }
                  )


@staff_member_required(login_url='login')
def edit_areas(request):
    paginator = Paginator(areas, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        CITY_NAME_SYNTAX_ERROR,
        AREA_NAME_SYNTAX_ERROR

    )
    search_result = ''
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        search_man_areas.setSearch(True)
        if request.POST.get('search_options') == 'city':
            search_message = request.POST.get('search_phrase')
            search_result = Area.objects.filter(
                city__name__icontains=search_message).order_by('id')
            search_man_areas.setPaginator(search_result)
            search_man_areas.setSearchPhrase(search_message)
            search_man_areas.setSearchOption('City')
            search_man_areas.setSearchError(False)

        elif request.POST.get('search_options') == 'area':
            search_message = request.POST.get('search_phrase')
            search_result = Area.objects.filter(
                name__icontains=search_message).order_by('id')
            search_man_areas.setPaginator(search_result)
            search_man_areas.setSearchPhrase(search_message)
            search_man_areas.setSearchOption('Area')
            search_man_areas.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter city name first!")
            search_man_areas.setSearchError(True)

    if request.method == "GET" and 'page' not in request.GET and not search_man_areas.getSearch():
        all_areas = Area.objects.all().order_by('id')
        search_man_areas.setPaginator(all_areas)
        search_man_areas.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_areas = Area.objects.filter().order_by('id')
        search_man_areas.setPaginator(all_areas)
        search_man_areas.setSearch(False)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = search_man_areas.getPaginator()
        areas_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        areas_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        areas_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/edit_areas.html',
                  {
                      'title': _('Edit Areas'),
                      'edit_areas': 'active',
                      'all_areas_data': areas_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': search_man_areas.getSearch(),
                      'search_result': search_result,
                      'search_phrase': search_man_areas.getSearchPhrase(),
                      'search_option': search_man_areas.getSearchOption(),
                      'search_error': search_man_areas.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "city_error": CITY_NAME_SYNTAX_ERROR,
                          "area_error": AREA_NAME_SYNTAX_ERROR
                      }
                  }
                  )


def edit_area(request, slug):
    from .models import Area
    from .forms import AreaForm
    # fetch the object related to passed id
    obj = get_object_or_404(Area, slug=slug)

    # pass the object as instance in form
    area_form = AreaForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if area_form.is_valid():
        area_form.save()
        name = area_form.cleaned_data.get('name')
        messages.success(request, f"Area {name} Updated")
    else:
        for field, items in area_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Area'),
        'edit_areas': 'active',
        'form': area_form,
        'area': obj,
    }
    return render(request, 'address/edit_area.html', context)


def confirm_area_delete(request, id):
    from .models import Area
    obj = get_object_or_404(Area, id=id)
    try:
        obj.delete()
        messages.success(request, f"Area {obj.name} deleted successfully")
    except:
        messages.error(request, f"Area {obj.name} was not deleted , please try again!")

    return redirect('deleteAreas')
