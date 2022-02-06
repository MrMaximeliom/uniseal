from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from apps.orders.models import Order
from Util.utils import SearchMan, ReportMan, delete_temp_folder
from Util.search_form_strings import NON_SELECTED_ORDER,ORDER_NOT_FOUND
orders = Order.objects.all().order_by('-id')
searchManObj = SearchMan("Order")
report_man = ReportMan()
def prepare_selected_query(selected_pages,paginator_obj,headers=None):
    categories_list = []
    products_list = []
    headers_here = ["Category", "Number of Products"]
    if headers is not None:
        print("in selected query headers are not none")
        headers_here = headers
        for header in headers_here:
            if header == "Category":
                for page in selected_pages:
                    for category in paginator_obj.page(page):
                        categories_list.append(category.name)
            elif header == "Number of Products":
                for page in selected_pages:
                    print("in for loop for supplier website")
                    for category in paginator_obj.page(page):
                        products_list.append(category.num_products)
    else:
        for page in range(1, paginator_obj.num_pages+1):
            for category in paginator_obj.page(page):
                products_list.append(category.num_products)
                categories_list.append(category.name)
    return headers_here, categories_list,products_list
def prepare_query(paginator_obj,headers=None):
    categories_list = []
    products_list = []
    headers_here = ["Category","Number of Products"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Category":
                for page in range(1, paginator_obj.num_pages+1):
                    for category in paginator_obj.page(page):
                        categories_list.append(category.name)
            elif header == "Number of Products":
                for page in range(1, paginator_obj.num_pages+1):

                    for category in paginator_obj.page(page):
                        products_list.append(category.num_products)
    else:

        for page in range(1, paginator_obj.num_pages+1):
            for category in paginator_obj.page(page):
                categories_list.append(category.name)
                products_list.append(category.num_products)
    return headers_here, categories_list, products_list

@staff_member_required(login_url='login')
def all_orders(request):
    from Util.ListsOfData import ORDER_STATUSES
    from Util.search_form_strings import CREATE_REPORT_TIP,CLEAR_SEARCH_TIP,SEARCH_ORDERS_TIP
    paginator = Paginator(orders, 5)
    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') != '' and request.POST.get('search_options') != 'none':
            search_message = request.POST.get('search_options')
            search_result = Order.objects.annotate(num_products=Count("order_details")).filter(
                status=search_message).order_by('-id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Order Status')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please select order status first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_orders = Order.objects.annotate(num_products=Count("order_details")).order_by('-id')
        searchManObj.setPaginator(all_orders)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_orders = Order.objects.annotate(num_products=Count("order_details")).order_by('-id')
        searchManObj.setPaginator(all_orders)
        searchManObj.setSearch(False)

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = searchManObj.getPaginator()
        orders_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        orders_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        orders_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'orders/all_orders.html',
                  {
                      'title': _('All Orders'),
                      'all_orders': 'active',
                      'orders':'active',
                      'all_orders_data': orders_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'order_statuses':ORDER_STATUSES,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'create_report_tip': CREATE_REPORT_TIP,
                      'clear_search_tip': CLEAR_SEARCH_TIP,
                      'search_orders_tip': SEARCH_ORDERS_TIP,
                      "not_found": ORDER_NOT_FOUND,
                      'data_js': {
                          "empty_search_phrase": NON_SELECTED_ORDER,


                      },
                  }
                  )
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

    if request.method == 'POST':
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
