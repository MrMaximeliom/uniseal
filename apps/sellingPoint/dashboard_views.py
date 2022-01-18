
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder


# Views for dashboard
def prepare_selected_query(selected_pages,paginator_obj,headers=None):
    point_name = []
    country = []
    state = []
    city = []
    area = []
    primary = []
    secondary = []
    email = []
    if headers is not None:
        headers_here = headers
        print(headers_here)
        for header in headers_here:
            if header == "Selling Point Name":
                for page in selected_pages:
                    for point in paginator_obj.page(page):
                        point_name.append(point.name)
            elif header == "Country":
                for page in selected_pages:
                    for point in paginator_obj.page(page):
                        country.append(point.description)
            elif header == "State":
                for page in selected_pages:
                    for point in paginator_obj.page(page):
                        state.append(point.state.name)
            elif header == "City":
                for page in selected_pages:
                    for point in paginator_obj.page(page):
                        city.append(point.city.name)
            elif header == "Area":
                for page in selected_pages:
                    for point in paginator_obj.page(page):
                        area.append(point.area.name)
            elif header == "Primary Phone":
                for page in selected_pages:
                    for point in paginator_obj.page(page):
                        primary.append(point.phone_number)
            elif header == "Secondary Phone":
                for page in selected_pages:
                    for point in paginator_obj.page(page):
                        secondary.append(point.secondary_phone)
            elif header == "Email":
                for page in selected_pages:

                    for point in paginator_obj.page(page):
                        email.append(point.email)
    else:
        headers_here = ["Selling Point Name", "Country", "State", "City", "Area","Primary Phone","Secondary Phone","Email"]
        print("headers are none in selected query")
        for page in range(1, paginator_obj.num_pages+1):
            for point in paginator_obj.page(page):
                point_name.append(point.name)
                country.append(point.country.name)
                state.append(point.state.name)
                city.append(point.city.name)
                area.append(point.area.name)
                primary.append(point.phone_number)
                secondary.append(point.secondary_phone)
                email.append(point.email)
    return headers_here, point_name, country,state,city,area,primary,secondary,email

def prepare_query(paginator_obj,headers=None):
    point_name = []
    country = []
    state = []
    city = []
    area = []
    primary = []
    secondary = []
    email = []
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Selling Point Name":
                for page in range(1, paginator_obj.num_pages+1):
                    for point in paginator_obj.page(page):
                        point_name.append(point.name)
            elif header == "Country":
                for page in range(1, paginator_obj.num_pages+1):
                    for point in paginator_obj.page(page):
                        country.append(point.country.name)
            elif header == "State":
                for page in range(1, paginator_obj.num_pages+1):
                    for point in paginator_obj.page(page):
                        state.append(point.state.name)
            elif header == "City":
                for page in range(1, paginator_obj.num_pages+1):
                    for point in paginator_obj.page(page):
                        city.append(point.city.name)
            elif header == "Area":
                for page in range(1, paginator_obj.num_pages+1):
                    for point in paginator_obj.page(page):
                        area.append(point.area.name)
            elif header == "Primary Phone":
                for page in range(1, paginator_obj.num_pages + 1):
                    for point in paginator_obj.page(page):
                        primary.append(point.phone_number)
            elif header == "Secondary Phone":
                for page in range(1, paginator_obj.num_pages + 1):
                    for point in paginator_obj.page(page):
                        secondary.append(point.secondary_phone)
            elif header == "Email":
                for page in range(1, paginator_obj.num_pages + 1):
                    for point in paginator_obj.page(page):
                        email.append(point.email)
    else:
        headers_here = ["Selling Point Name","Country","State","City","Area","Primary Phone","Secondary Phone","Email"]
        for page in range(1, paginator_obj.num_pages+1):
            for point in paginator_obj.page(page):
                point_name.append(point.name)
                country.append(point.country.name)
                state.append(point.state.name)
                city.append(point.city.name)
                area.append(point.area.name)
                primary.append(point.phone_number)
                secondary.append(point.secondary_phone)
                email.append(point.email)

    # later for extracting actual data


    return headers_here,point_name,country,state,city,area,primary,secondary,email

from apps.sellingPoint.models import SellingPoint
sellingPoints = SellingPoint.objects.all().order_by("id")
searchManObj = SearchMan("Selling Point")
report_man = ReportMan()
@staff_member_required(login_url='login')
def all_selling_points(request):
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        CITY_NAME_SYNTAX_ERROR,
    COUNTRY_NAME_SYNTAX_ERROR,
    STATE_NAME_SYNTAX_ERROR,
    AREA_NAME_SYNTAX_ERROR,
    POINT_NAME_SYNTAX_ERROR

    )
    # all_points = SellingPoint.objects.all().order_by("id")
    # paginator = Paginator(all_points, 5)
    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        print("delete reports")
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
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
    if request.method == "GET" and 'page' not in request.GET and not searchManObj.getSearch():
        all_points = SellingPoint.objects.all().order_by("id")
        searchManObj.setPaginator(all_points)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_points = SellingPoint.objects.all().order_by("id")
        searchManObj.setPaginator(all_points)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Selling Point Name") if request.POST.get('name_header') is not None else ''
        headers.append("Country") if request.POST.get('country_header') is not None else ''
        headers.append("State") if request.POST.get('state_header') is not None else ''
        headers.append("City") if request.POST.get('city_header') is not None else ''
        headers.append("Area") if request.POST.get('area_header') is not None else ''
        headers.append("Primary Phone") if request.POST.get('primary_phone_header') is not None else ''
        headers.append("Secondary Phone") if request.POST.get('secondary_phone_header') is not None else ''
        headers.append("Email") if request.POST.get('email_header') is not None else ''
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                constructor = {}
                headers, point_name, country, state, city,area, primary,secondary,email = prepare_selected_query(
                    selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                if len(point_name) > 0:
                    constructor.update({"point_name": point_name})
                if len(country) > 0:
                    constructor.update({"country": country})
                if len(state) > 0:
                    constructor.update({"state": state})
                if len(city) > 0:
                    constructor.update({"city": city})
                if len(area) > 0:
                    constructor.update({"area": area})
                if len(primary) > 0:
                    constructor.update({"primary": primary})
                if len(secondary) > 0:
                    constructor.update({"secondary": primary})
                if len(email) > 0:
                    constructor.update({"email": email})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Selling_Points',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers = ["Selling Point Name", "Country", "State", "City", "Area","Primary Phone","Secondary Phone","Email"]

                headers, point_name, country, state, city,area, primary,secondary,email = prepare_selected_query(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Selling_Points',
                                                                                  headers, point_name=point_name,
                                                                                  country=country,
                                                                                  state=state,
                                                                                  city=city,
                                                                                  area=area,
                                                                                  primary=primary,
                                                                                  secondary=secondary,
                                                                                  email=email
                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            query = searchManObj.getPaginator()
            if len(headers) > 0:
                constructor = {}
                headers, point_name, country, state, city,area, primary,secondary,email = prepare_query(query,
                                                                                                   headers=headers)
                if len(point_name) > 0:
                    constructor.update({"point_name": point_name})
                if len(country) > 0:
                    constructor.update({"country": country})
                if len(state) > 0:
                    constructor.update({"state": state})
                if len(city) > 0:
                    constructor.update({"city": city})
                if len(area) > 0:
                    constructor.update({"area": area})
                if len(primary) > 0:
                    constructor.update({"primary": primary})
                if len(secondary) > 0:
                    constructor.update({"secondary": secondary})
                if len(email) > 0:
                    constructor.update({"email": email})
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
                headers, point_name, country, state, city,area, primary,secondary,email = prepare_query(query)
                status, filePath, fileName = createExelFile('Report_For_Selling_Points',
                                                            headers, point_name=point_name,
                                                            country=country,
                                                            state=state,
                                                            city=city,
                                                            area=area,
                                                            primary=primary,
                                                            secondary=secondary,
                                                            email=email,

                                                            )
                report_man.setFileName(fileName)
                report_man.setFilePath(filePath)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(sellingPoints, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        selling_points = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        selling_points = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        selling_points = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sellingPoints/all_selling_points.html',
                  {
                      'title': _('All Selling Points'),
                      'selling_points':'active',
                      'all_selling_points': 'active',
                      'all_selling_points_data': selling_points,
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
                          "point_error": POINT_NAME_SYNTAX_ERROR,
                          "country_error": COUNTRY_NAME_SYNTAX_ERROR,
                          "state_error": STATE_NAME_SYNTAX_ERROR,
                          "city_error":CITY_NAME_SYNTAX_ERROR,
                          "area_error":AREA_NAME_SYNTAX_ERROR,

                      }

                  }
                  )
@staff_member_required(login_url='login')
def add_selling_points(request):
    from .forms import SellingPointForm
    if request.method == 'POST':
        form = SellingPointForm(request.POST,request.FILES)
        if form.is_valid():
            # point = form.save()
            # point.slug = slugify(rand_slug())
            # point.save()
            form.save()
            point_name = form.cleaned_data.get('name')
            messages.success(request, f"Successfully Added Selling Point : {point_name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = SellingPointForm()

    context = {
        'title': _('Add Selling Points'),
        'add_selling_points': 'active',
        'form': form,
        'selling_points': 'active',
    }
    return render(request, 'sellingPoints/add_selling_points.html', context)
@staff_member_required(login_url='login')
def delete_selling_points(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(sellingPoints, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        selling_points = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        selling_points = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        selling_points = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sellingPoints/delete_selling_points.html',
                  {
                      'title': _('Delete Selling Points'),
                      'all_selling_points': 'active',
                      'selling_points': 'active',
                      'all_selling_points_data': selling_points,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@staff_member_required(login_url='login')
def edit_selling_points(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(sellingPoints, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        selling_points = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        selling_points = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        selling_points = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sellingPoints/edit_selling_points.html',
                  {
                      'title': _('Edit Selling Points'),
                      'all_selling_points': 'active',
                      'selling_points': 'active',
                      'all_selling_points_data': selling_points,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@staff_member_required(login_url='login')
def edit_selling_point(request,slug):
    from .models import SellingPoint
    from .forms import SellingPointForm
    obj = get_object_or_404(SellingPoint, slug=slug)

    # pass the object as instance in form
    point_form = SellingPointForm(request.POST or None, instance=obj)
    # save the data from the form and
    # redirect to detail_view
    if point_form.is_valid()  :
        if request.FILES:
            project = point_form.save()
            project.image = request.FILES['image']
            project.save()
        point_form.save()
        point_name = point_form.cleaned_data.get('name')
        messages.success(request, f"Successfully Updated : {point_name} Data")
    else:
        for field, items in point_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Selling Points'),
        'edit_selling_points': 'active',
        'form':point_form,
        'selling_point' : obj,
        'selling_points': 'active',

    }
    return render(request, 'sellingPoints/edit_selling_point.html', context)

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
@staff_member_required(login_url='login')
def confirm_delete(request,id):
    from .models import SellingPoint
    obj = get_object_or_404(SellingPoint, id=id)
    try:
        obj.delete()
        messages.success(request, f"Selling Point: {obj.name} deleted successfully")
    except:
        messages.error(request, f"Selling Point: {obj.name} was not deleted , please try again!")


    return redirect('deleteSellingPoints')