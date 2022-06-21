from pathlib import Path

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from reportlab.lib.pagesizes import letter

from Util.ListsOfData import ORDER_STATUSES
from Util.utils import (SearchMan,
                        createExelFile,
                        ReportMan,
                        delete_temp_folder,
                        get_fields_names_for_report_file,
                        get_selected_pages,
                        prepare_default_query,
                        prepare_selected_query)
from Util.search_form_strings import NON_SELECTED_ORDER, ORDER_NOT_FOUND
from apps.orders.models import Order
from apps.common_code.views import BaseListView

from Util.search_form_strings import ORDER_NOT_FOUND
orders = Order.objects.all().order_by('-id')
# search_object = SearchMan("Order")
report_man = ReportMan()

class OrderListView(BaseListView):
    def get(self, request, *args, **kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        ssearch_object = SearchMan(self.model_name)
        queryset = ssearch_object.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session:
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            instances = ssearch_object.get_queryset()
            ssearch_object.setPaginator(instances)
            ssearch_object.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = ssearch_object.getPaginator()
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
            'search': ssearch_object.getSearch(),
            'search_result': search_result,
            'search_phrase': ssearch_object.getSearchPhrase(),
            'search_option': ssearch_object.getSearchOption(),
            'search_error': ssearch_object.getSearchError(),
            'create_report_tip': CREATE_REPORT_TIP,
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'order_statuses': ORDER_STATUSES,
            'data_js': {
                "empty_search_phrase": EMPTY_SEARCH_PHRASE,
            }
        }
        return super().get(request)
    def post(self,request,*args,**kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        search_object = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if  'clear' not in request.POST and 'createExcel' not in request.POST:
            search_object.setSearch(True)
        if  request.POST.get('clear') == 'clear':
            instances = search_object.get_queryset()
            search_object.setPaginator(instances)
            search_object.setSearch(False)
        if 'clear' not in request.POST and 'createExcel' not in request.POST:
            search_object.setSearch(True)
            if request.POST.get('search_options') != '' and request.POST.get('search_options') != 'none':
                search_message = request.POST.get('search_options')
                print("searched")
                print("searched value",search_message)
                search_result = Order.objects.annotate(number_of_products=Count("order_details")).filter(
                    status__icontains=search_message).order_by('-id')
                search_object.setPaginator(search_result)
                search_object.setSearchPhrase(search_message)
                search_object.setSearchOption('Order Status')
                search_object.setSearchError(False)

            else:
                messages.error(request,
                               "Please select order status first!")
                search_object.setSearchError(True)


        if  request.POST.get('createExcel') == 'done':
            headers = []

            headers.append("user") if request.POST.get('user_header') is not None else ''
            headers.append("total") if request.POST.get('total_header') is not None else ''
            headers.append("created_at") if request.POST.get('created_at_header') is not None else ''
            headers.append("modified_at") if request.POST.get('modified_at_header') is not None else ''
            headers.append("status") if request.POST.get('status_header') is not None else ''
            headers.append("number_of_products") if request.POST.get('products_header') is not None else ''

            # create report functionality
            # setting all data as default behaviour
            if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
                # get requested pages from the paginator of original page
                selected_pages = get_selected_pages(request.POST.get('pages_collector'))
                query = search_object.getPaginator()
                if len(headers) > 0:
                    constructor = prepare_selected_query(search_object.get_queryset(),headers,selected_pages,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Orders',
                                                                                      headers, **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


                else:
                    headers = ["user","total","created_at","modified_at","status","number_of_products"]
                    constructor = prepare_selected_query(search_object.get_queryset(),headers,selected_pages,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Orders',
                                                                                      headers,
                                                                                      **constructor
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
                query = search_object.getPaginator()
                if len(headers) > 0:
                    constructor = prepare_default_query(search_object.get_queryset(),headers,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Orders',
                                                                                      headers, **constructor)
                    if status:

                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")

                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

                else:
                    headers = ["user","total","created_at","modified_at","status","number_of_products"]
                    constructor = prepare_default_query(search_object.get_queryset(),headers,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Orders',
                                                                                      headers,
                                                                                      **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created")
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))

        else:
            page = None
        try:
            paginator = search_object.getPaginator()
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
                'search': search_object.getSearch(),
                'search_result': search_result,
                'search_phrase': search_object.getSearchPhrase(),
                'search_option': search_object.getSearchOption(),
                'search_error': search_object.getSearchError(),
                'create_report_tip': CREATE_REPORT_TIP,
                'clear_search_tip': CLEAR_SEARCH_TIP,
                'order_statuses': ORDER_STATUSES,
                'not_found':ORDER_NOT_FOUND,
                'data_js': {
                    "empty_search_phrase": EMPTY_SEARCH_PHRASE,

                }
            }
        return super().get(request)


@staff_member_required(login_url='login')
def edit_order(request, slug):
    from Util.ListsOfData import ORDER_STATUSES
    from apps.orders.models import Order, Cart
    order = get_object_or_404(Order, slug=slug)
    order_carts = Cart.objects.filter(order=order)

    # calculating total price for order
    total = 0.0
    product_total = list()
    if order_carts:
        for cart in order_carts:
            product_total.append(cart.quantity * cart.product.price)
            total += (cart.quantity * cart.product.price)
    if 'temp_dir' in request.session:
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if  request.method == 'POST' and "update_order" not in request.POST and request.POST.get('create-order-report') != 'none' and request.POST.get('create-order-report') != '':
        request.session['temp_dir'] = 'delete man!'
        complete_file_path,file_name = create_report(request, request.POST.get('create-order-report'))
        return redirect('downloadReport', str(complete_file_path), str(file_name))

    if request.method == 'POST' and "create-order-report" not in request.POST and request.POST.get("update_order") != 'none' and request.POST.get("update_order") != '' :
        order_status = request.POST.get('order_status')
        Order.objects.filter(slug=slug).update(status=order_status)
        messages.success(request, f"Order {order.slug} was successfully updated!")

    return render(request, 'orders/order_details.html',
                  {
                      'title': _('Order Details'),
                      'order_details': 'active',
                      'order': order,
                      'carts': order_carts,
                      'total': total,
                      'order_statuses':ORDER_STATUSES
                  }
                  )

@staff_member_required(login_url='login')
def create_report(request, slug):
    import os
    from reportlab.platypus import SimpleDocTemplate,Table
    from apps.orders.models import Order,Cart
    from datetime import datetime
    path = str(Path(__file__).resolve().parent.parent) + str("/OrdersReports")
    print("path is: ",path)
    file_name = 'order_report_'+str(datetime.now().second)+ ".pdf"
    print(file_name)

    complete_file_path = os.path.abspath(path) + "/" + file_name
    print("complete path is: ",complete_file_path)
    order = get_object_or_404(Order, slug=slug)
    user_details_headers = ["Full Username","Phone Number","Email"]
    user_details = []
    user_details.append(order.user.username)
    user_details.append(order.user.phone_number)
    user_details.append(order.user.email)
    order_details_headers = ["Product Name","Product Price","Quantity","Total"]
    order_product_names = []
    order_product_prices = []
    order_product_quantities = []
    order_product_totals = []
    order_carts = Cart.objects.filter(order=order)
    order_data = []
    order_data.append(order_details_headers)
    for product in order_carts:
        temp_arr = []
        temp_arr.append(product.product.name)
        temp_arr.append(product.product.price)
        temp_arr.append(product.quantity)
        temp_arr.append(product.quantity*product.product.price)
        order_data.append(temp_arr)
    pdf = SimpleDocTemplate(
        complete_file_path,
        pagesize=letter,
    )
    from reportlab.platypus import Table
    print("quantities are ",order_product_quantities)
    print("totals are ",order_product_quantities)
    user_data = [
        user_details_headers,
        user_details
    ]

    order_table = Table(order_data)
    elems = []
    elems.append(order_table)
    pdf.build(elems)
    return complete_file_path,file_name



