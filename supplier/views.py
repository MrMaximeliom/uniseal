from django.template.defaultfilters import slugify
from rest_framework import viewsets
from Util.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from Util.utils import  SearchMan,createExelFile,ReportMan,delete_temp_folder

# Create your views here.
class SupplierViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify suppliers' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Other users can only use GET function on this endpoint
    Data will be retrieved in the following format for GET function:
    {
     "id":11,
     "name": "supplier_name",
     "image": "supplier_image_url",
     }
     Use other functions by accessing this url:
     supplier/<supplier's_id>
     Format of data will be as the previous data format for GET function
     To Search for particular supplier by its name use this url:
     supplier/?name=<supplier_name>
    """

    def get_view_name(self):
        return _("Create/Modify Suppliers' Data")


    from .serializers import SupplierSerializer
    serializer_class = SupplierSerializer

    def get_queryset(self):
        from .models import Supplier
        queryset = Supplier.objects.all().order_by("id")
        return queryset
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


# Dashboard Views
from .models import Supplier, rand_slug
from django.contrib.admin.views.decorators import staff_member_required


suppliers = Supplier.objects.all().order_by("id")
searchManObj = SearchMan("Supplier")
report_man = ReportMan()
# report_man.setTempDir(tempfile.mkdtemp())
def prepare_selected_query(selected_pages,paginator_obj,headers=None):
    link_list = []
    supplier_list = []
    headers_here = ["Supplier Name", "Supplier Website"]
    if headers is not None:
        print("in headers section of selected query")
        headers_here = headers
        for header in headers_here:
            if header == "Supplier Name":
                for page in selected_pages:
                    for supplier in paginator_obj.page(page):
                        supplier_list.append(supplier.name)
            elif header == "Supplier Website":
                print("here in supplier website")
                for page in selected_pages:
                    print("in for loop for supplier website")
                    for supplier in paginator_obj.page(page):
                        print("appending supplier links")
                        link_list.append(supplier.link)
    else:
        print("in else section of selected query")
        for page in range(1, paginator_obj.num_pages+1):
            for supplier in paginator_obj.page(page):
                link_list.append(supplier.link)
                supplier_list.append(supplier.name)


    return headers_here, supplier_list , link_list
def prepare_query(paginator_obj,headers=None):
    supplier_list = []
    link_list = []
    headers_here = ["Supplier Name","Supplier Website"]
    if headers is not None:
        print("in headers section of prepare query")
        headers_here = headers
        for header in headers_here:
            if header == "Supplier Name":
                for page in range(1, paginator_obj.num_pages+1):
                    for supplier in paginator_obj.page(page):
                        supplier_list.append(supplier.name)
            elif header == "Supplier Website":
                for page in range(1, paginator_obj.num_pages+1):
                    for supplier in paginator_obj.page(page):
                        link_list.append(supplier.link)
    else:
        print("in else section of prepare query")
        for page in range(1, paginator_obj.num_pages+1):
            for supplier in paginator_obj.page(page):
                supplier_list.append(supplier.name)
                link_list.append(supplier.link)
    return headers_here, supplier_list, link_list
@staff_member_required(login_url='login')
def all_suppliers(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(suppliers, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
    SUPPLIER_NAME_SYNTAX_ERROR

    )
    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Supplier.objects.filter(name=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Supplier Name')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter supplier name first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET  and not searchManObj.getSearch():
        all_suppliers = Supplier.objects.all().order_by("id")
        searchManObj.setPaginator(all_suppliers)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_suppliers = Supplier.objects.all().order_by("id")
        searchManObj.setPaginator(all_suppliers)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Supplier Name")
        headers.append("Supplier Website")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none':
            print("pages collector is not none")
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                print('in page selectors')
                if item != ",":
                    selected_pages.append(item)
            print("selected pages are: ",selected_pages)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, supplier ,link = prepare_selected_query(
                    selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                print("suppliers: ",supplier,"\n","links: ",link)
                if len(supplier) > 0:
                    constructor.update({"supplier": supplier})
                if len(link) > 0:
                    constructor.update({"link": link})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Suppliers',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers = ["Supplier Name", "Supplier Website"]
                headers, supplier , link = prepare_selected_query(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Suppliers',
                                                                                  headers, supplier=supplier,
                                                                                  link=link
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
            print("pages collector is none")
            query = searchManObj.getPaginator()
            if len(headers) > 0:
                constructor = {}
                headers,  supplier , link = prepare_query(query,headers=headers)
                if len(supplier) > 0:
                    constructor.update({"supplier": supplier})
                if len(link) > 0:
                    constructor.update({"link": link})
                status, report_man.filePath, report_man.fileName = createExelFile( 'Report_For_Suppliers',
                                                                                  headers, **constructor)
                if status:
                   # request.session['temp_dir'] = report_man.tempDir
                   request.session['temp_dir'] = 'delete man!'
                   messages.success(request, f"Report Successfully Created ")
                   # return redirect('download_file',filepath=filepath,filename=filename)

                   return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                   messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                headers, supplier,link = prepare_query(query)
                status, report_man.filePath, report_man.fileName = createExelFile( 'Report_For_Suppliers',
                                                                                  headers,supplier=supplier,
                                                                                  link=link)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                   messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        supplier_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        supplier_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        supplier_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'supplier/all_suppliers.html',
                  {
                      'title': _('All Suppliers'),
                      'all_suppliers': 'active',
                      'all_suppliers_data': supplier_data,
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
                          "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,
                      }
                  }
                  )
@staff_member_required(login_url='login')
def edit_suppliers(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
    SUPPLIER_NAME_SYNTAX_ERROR

    )
    search_result = ''
    paginator = Paginator(suppliers, 5)
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Supplier.objects.filter(name=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Supplier Name')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter supplier name first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET  and not searchManObj.getSearch():
        all_suppliers = Supplier.objects.all().order_by("id")
        searchManObj.setPaginator(all_suppliers)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_suppliers = Supplier.objects.all().order_by("id")
        searchManObj.setPaginator(all_suppliers)
        searchManObj.setSearch(False)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        supplier_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        supplier_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        supplier_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'supplier/edit_suppliers.html',
                  {
                      'title': _('Edit Suppliers'),
                      'edit_suppliers': 'active',
                      'all_suppliers_data': supplier_data,
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
                          "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,
                      }
                  }
                  )

@staff_member_required(login_url='login')
def add_suppliers(request):
    from .forms import SupplierForm
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()
            form.slug = slugify(rand_slug())
            form.save()
            supplier_name = form.cleaned_data.get('name')
            messages.success(request, f"New Supplier Added: {supplier_name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = SupplierForm()


    context = {
        'title': _('Add Suppliers'),
        'add_suppliers': 'active',
        'form': form,
    }
    return render(request, 'supplier/add_suppliers.html', context)
@staff_member_required(login_url='login')
def delete_suppliers(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(suppliers, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
    SUPPLIER_NAME_SYNTAX_ERROR

    )
    search_result = ''
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Supplier.objects.filter(name=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Supplier Name')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter supplier name first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET  and not searchManObj.getSearch():
        all_suppliers = Supplier.objects.all().order_by("id")
        searchManObj.setPaginator(all_suppliers)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_suppliers = Supplier.objects.all().order_by("id")
        searchManObj.setPaginator(all_suppliers)
        searchManObj.setSearch(False)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        supplier_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        supplier_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        supplier_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'supplier/delete_suppliers.html',
                  {
                      'title': _('Delete Suppliers'),
                      'delete_suppliers': 'active',
                      'all_suppliers_data': supplier_data,
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
                          "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,
                      }
                  }
                  )

@staff_member_required(login_url='login')
def edit_supplier(request,slug):
    from supplier.models import Supplier
    from .forms import SupplierForm
    obj = get_object_or_404(Supplier, slug=slug)
    print(obj.name)
    # if request.FILES['image']:

    supplier_form = SupplierForm(request.POST or None, instance=obj)
    if supplier_form.is_valid():
        if request.FILES:
            supplier = supplier_form.save()
            supplier.image = request.FILES['image']
            supplier.save()
        supplier_form.save()
        name = supplier_form.cleaned_data.get('name')
        messages.success(request, f"Successfully Updated : {name} Data")
    else:
        for field, items in supplier_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))
    context = {
        'title': _('Edit Suppliers'),
        'edit_suppliers': 'active',
        'all_suppliers': suppliers,
        'form':supplier_form,
        'supplier':obj
    }
    return render(request, 'supplier/edit_supplier.html', context)
@staff_member_required(login_url='login')
def confirm_delete(request,id):
    from supplier.models import Supplier
    obj = get_object_or_404(Supplier, id=id)
    try:
        obj.delete()
        messages.success(request, f"Supplier {obj.name} deleted successfully")
    except:
        messages.error(request, f"Supplier {obj.name} was not deleted , please try again!")


    return redirect('deleteSuppliers')