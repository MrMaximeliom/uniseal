from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from Util.utils import (SearchMan, createExelFile, ReportMan,
                        delete_temp_folder,
                        get_selected_pages,
                        prepare_default_query,
                        prepare_selected_query,
                        get_fields_names_for_report_file)
from Util.utils import rand_slug
from apps.common_code.views import BaseListView
from apps.product.models import Product


class ProductListView(BaseListView):
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
            if request.POST.get('search_options') == 'product':
                print('here now in product search')
                search_message = request.POST.get('search_phrase')
                search_result = Product.objects.filter(name__icontains=search_message).order_by('id')
                print("search results ", search_result)
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('Product Name')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'category':
                print('here now in category search')
                search_phrase = request.POST.get('search_phrase')
                search_result = Product.objects.filter(category__name__icontains=search_phrase).order_by("id")
                print("search results ", search_result)
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('Category')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'supplier':
                print('here now in supplier search')
                search_phrase = request.POST.get('search_phrase')
                print('search phrase is ', search_phrase)
                search_result = Product.objects.filter(supplier__name__icontains=search_phrase).order_by("id")
                print("search results ", search_result)
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('Supplier')
                searchManObj.setSearchError(False)
            else:
                messages.error(request,
                               "Please choose an item from list , then write search phrase to search by it!")
                searchManObj.setSearchError(True)

        if request.POST.get('clear') == 'clear':
            instances = searchManObj.get_queryset()
            searchManObj.setPaginator(instances)
            searchManObj.setSearch(False)

        if request.method == "POST" and request.POST.get('createExcel') == 'done':
            headers = []
            headers.append("name") if request.POST.get('product_header') is not None else ''
            headers.append("category") if request.POST.get('category_header') is not None else ''
            headers.append("supplier") if request.POST.get('supplier_header') is not None else ''
            headers.append("description") if request.POST.get('description_header') is not None else ''
            headers.append("added_date") if request.POST.get('added_date_header') is not None else ''
            # create report functionality
            # setting all data as default behaviour
            if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
                # get requested pages from the paginator of original page
                selected_pages = get_selected_pages(request.POST.get('pages_collector'))
                query = searchManObj.getPaginator()
                if len(headers) > 0:
                    constructor = prepare_selected_query(searchManObj.get_queryset(),headers,selected_pages,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Products',
                                                                                      headers, **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


                else:
                    headers = get_fields_names_for_report_file(Product,Product.get_not_wanted_fields_names_in_report_file())
                    constructor = prepare_selected_query(searchManObj.get_queryset(),headers,selected_pages,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Products',
                                                                                      headers,
                                                                                      **constructor)
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
                    print("place one")
                    constructor = prepare_default_query(searchManObj.get_queryset(),headers,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Products',
                                                                                      headers, **constructor)
                    if status:

                        messages.success(request, f"Report Successfully Created ")
                        request.session['temp_dir'] = 'delete man!'
                        # return redirect('download_file',filepath=filepath,filename=filename)

                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

                else:
                    print("place two")
                    headers = get_fields_names_for_report_file(Product,Product.get_not_wanted_fields_names_in_report_file())
                    constructor = prepare_default_query(searchManObj.get_queryset(),headers,query)
                    status, filePath, fileName = createExelFile('Report_For_Products',
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


# ends here



searchManObj = SearchMan("Product")
report_man = ReportMan()



@staff_member_required(login_url='login')
def product_details(request, slug):
    from apps.product.models import Product, ProductImages
    product = get_object_or_404(Product, slug=slug)
    productImages = ProductImages.objects.filter(product__slug=slug)
    pureImages = list()
    if productImages:
        pureImages.append(product.image.url)
        for image in productImages:
            pureImages.append(image.image.url)

    if request.method == "GET":
        if productImages:
            print("its noot empty yo!")
            print(product.image.url)
        else:
            print("its emmpty yoooo!")

    return render(request, 'product/product_detail.html',
                  {
                      'title': _('Product Details'),
                      'all_products': 'active',
                      'products': 'active',
                      'product_data': product,
                      'product_images': pureImages,
                      'product_original_image': product.image.url

                  }
                  )


@staff_member_required(login_url='login')
def product_images(request, slug=None):
    from apps.product.models import Product, ProductImages
    import os
    from django.db.models import Count
    from .forms import ProductImagesForm
    allProducts = Product.objects.all()
    pureImages = {}
    context = {
        'title': _('Product Images'),
        'product_images_base': 'active',
        'allProducts': allProducts,
        'products': 'active',
    }
    if slug != None and request.method == 'GET':
        product = get_object_or_404(Product, slug=slug)
        productImages = ProductImages.objects.filter(product__slug=slug)
        if productImages:
            # pureImages.append(project.image.url)
            pureImages.update({True: product.image.url})
            for image in productImages:
                # pureImages.append(image.image.url)
                pureImages.update({image.image.url: image.image.url})
        print(pureImages)
        context = {
            'title': _('Product Images'),
            'product_images_base': 'active',
            'product_data': product,
            'product_images': pureImages,
            'product_original_image': product.image.url,
            'allProducts': allProducts,
            'slug': slug
        }
        form = ProductImagesForm()
        context.update({"form": form})

    if request.method == 'POST' and 'search_product' in request.POST:
        if request.POST.get('search_options') != 'none':
            chosen_project = request.POST.get('search_options')
            # project = get_object_or_404(Project,slug=chosen_project)
            # projectImages = ProjectImages.objects.filter(project__slug=chosen_project)
            return redirect('productImages', slug=chosen_project)
        else:
            messages.error(request, "Please choose a product from the list")

    if request.method == 'POST' and 'add_images' in request.POST:
        form = ProductImagesForm(request.POST, request.FILES)
        product = get_object_or_404(Product, slug=slug)
        selected_product = Product.objects.filter(slug=slug)
        files = request.FILES.getlist('image')
        form.product = selected_product
        if form.is_valid():
            if len(files) == 1:

                updated_product = form.save(commit=False)
                updated_product.image = request.FILES['image']
                # updated_project.project = selected_project.id
                updated_product.slug = slugify(rand_slug())
                # updated_project.save()
                product_name = product.name
                messages.success(request, f"New image Added for: {product_name}")

            else:
                for f in files:
                    ProductImages.objects.create(product=product, image=f)
                product_name = product.name
                messages.success(request, f"New images Added for: {product_name}")
            return redirect('productImages', slug=slug)
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

    if request.method == 'POST' and 'confirm_changes' in request.POST:
        product_instances = ProductImages.objects.annotate(num_products=Count('product')).filter(product__slug=slug)
        all_product_images_count = product_instances.count() + 1
        default_image = request.POST.get('posted_default_image')
        deleted_images = request.POST.get('posted_deleted_images')
        print("default image is: ", default_image)
        # handling default image first
        current_product = Product.objects.get(slug=slug)
        current_default_image = current_product.image
        if default_image != 'none':
            if current_default_image != default_image:
                default_image_path = default_image
                just_image_path = default_image_path.split('/media')
                Product.objects.filter(slug=slug).update(image=just_image_path[1])
                ProductImages.objects.create(product=current_product, image=just_image_path[1])

        if deleted_images != 'none':
            # check that the selected images are not greater than all of the project's images
            print("deleted images are: ", deleted_images.split(','))
            print("now deleting images ")
            for instance in product_instances:
                for image in deleted_images.split(','):
                    # print("first image: ",instance.image.url)
                    # print("second image: ",image)
                    if instance.image.url == image:
                        deleted_image_path = os.path.dirname(os.path.abspath('unisealAPI')) + image
                        deleted_record = ProductImages.objects.get(id=instance.id)
                        deleted_record.delete()
                        if os.path.exists(deleted_image_path):
                            os.remove(deleted_image_path)

        messages.success(request, f"Product {current_product.name} was successfully updated!")
        return redirect('productImages', slug=slug)

    return render(request, 'product/product_images.html',
                  context

                  )


class TopProductsHelper:
    query = ''

    def setQuery(self, query):
        self.query = query

    def getQuery(self):
        return self.query


top_products_helper = TopProductsHelper()


@staff_member_required(login_url='login')
def top_products(request):
    from apps.product.models import Product
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        PRODUCT_NAME_SYNTAX_ERROR,
        CATEGORY_NAME_SYNTAX_ERROR,
        SUPPLIER_NAME_SYNTAX_ERROR,
        PRODUCT_NOT_FOUND,
        CLEAR_SEARCH_TIP,
        CREATE_REPORT_TIP,
        SEARCH_PRODUCTS_TIP,

    )
    all_products = Product.objects.filter(is_top=True).order_by("id")
    top_products_helper.setQuery(all_products)
    search_result = ''
    displaying_type = 'Top Products'
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST and 'updating_top_products' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'product':
            print('here now in product search')
            search_message = request.POST.get('search_phrase')
            search_result = Product.objects.filter(name__icontains=search_message).order_by('id')
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Product Name')
            searchManObj.setSearchError(False)
            top_products_helper.setQuery(search_result)
        elif request.POST.get('search_options') == 'category':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = Product.objects.filter(category__name__icontains=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)
            top_products_helper.setQuery(search_result)
        elif request.POST.get('search_options') == 'supplier':
            print('here now in supplier search')
            search_phrase = request.POST.get('search_phrase')
            print('search phrase is ', search_phrase)
            search_result = Product.objects.filter(supplier__name__icontains=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Supplier')
            searchManObj.setSearchError(False)
            top_products_helper.setQuery(search_result)
        elif request.POST.get('search_options') == 'top_products':
            search_phrase = request.POST.get('search_phrase')
            search_result = Product.objects.filter(is_top=True, name__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Top Products')
            searchManObj.setSearchError(False)
            top_products_helper.setQuery(search_result)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not searchManObj.getSearch():
        print("iam here now")
        all_products = Product.objects.filter(is_top=True).order_by("id")
        searchManObj.setPaginator(all_products)
        searchManObj.setSearch(False)
        top_products_helper.setQuery(all_products)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_products = Product.objects.filter(is_top=True).order_by("id")
        searchManObj.setPaginator(all_products)
        searchManObj.setSearch(False)
        top_products_helper.setQuery(all_products)
    if request.method == 'POST' and 'updating_top_products' in request.POST:
        print("here now updating top products")
        searchManObj.setSearch(False)
        selected_top_products = request.POST.get('selected_top_products')
        deleted_top_products = request.POST.get('deleted_top_products')
        print("selected products are: ", selected_top_products)
        print("deleted top products are: ", deleted_top_products)
        updated = False
        if selected_top_products != 'none':
            selected_products = list()
            # selected_products_ids = request.POST.get('selected_top_products')
            for product_id in selected_top_products.split(','):
                print(product_id)
            from apps.product.models import Product
            for product_id in selected_top_products.split(','):
                selected_products.append(
                    Product.objects.get(id=product_id)
                )
            print("selected products are: \n")
            print(selected_products)
            for product in selected_products:
                product.is_top = True
            Product.objects.bulk_update(selected_products, ['is_top'])
        if deleted_top_products != 'none':
            deleted_products = list()
            # selected_products_ids = request.POST.get('selected_top_products')
            print("deleted top products are: ", deleted_top_products)
            print("\ndeleted top products splited: ", deleted_top_products.split(','))
            print("\n cycling throw splited products")
            for product_id in deleted_top_products.split(','):
                print(product_id)
            from apps.product.models import Product
            for product_id in deleted_top_products.split(','):
                deleted_products.append(
                    Product.objects.get(id=product_id)
                )
            print("selected products are: \n")
            print(deleted_products)
            for product in deleted_products:
                product.is_top = False
            Product.objects.bulk_update(deleted_products, ['is_top'])
        if updated:
            messages.success(request, "Top Products Updated Successfully!")

    return render(request, 'product/top_products.html',
                  {
                      'title': _('Top Products'),
                      'top_products': 'active',
                      'products': 'active',
                      'all_products_data': top_products_helper.getQuery(),
                      'displaying_type': displaying_type,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'create_report_tip': CREATE_REPORT_TIP,
                      'clear_search_tip': CLEAR_SEARCH_TIP,
                      'search_products_tip': SEARCH_PRODUCTS_TIP,
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "product_error": PRODUCT_NAME_SYNTAX_ERROR,
                          "category_error": CATEGORY_NAME_SYNTAX_ERROR,
                          "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,

                      },
                      'not_found': PRODUCT_NOT_FOUND,
                  }
                  )
