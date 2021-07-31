from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from Util.permissions import UnisealPermission
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
from Util.utils import rand_slug


class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify products' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":11,
     "name": "product_name",
     "image": "product_image_url",
     "product_file":"product_file_url",
     "description":"Product_description",
     "added_date":"added_date"
     "category":category_id,
     "supplier":"supplier_id",
     }
     Use other functions by accessing this url:
     product/modifyProduct/<product's_id>
     Format of data will be as the previous data format for GET function
     To Get Products By Category use this url:
     product/modifyProduct/?category=<category_id>
     To Get Products By Supplier use this url:
     product/modifyProduct/?supplier=<supplier_id>
     To Get Products By Both Category and Supplier use this url:
     product/modifyProduct/?category=<category_id>&supplier=<supplier_id>

    """

    def get_view_name(self):
        return _("Create/Modify Products' Data")

    # def get_queryset(self):
    #     from .models import Product
    #     # returning default result if anything goes wrong
    #     queryset = Product.objects.all().order_by("id")
    #     return queryset

    from .serializers import ProductSerializer
    serializer_class = ProductSerializer
    from .models import Product
    permission_classes = [UnisealPermission]
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'supplier']


class ProductImagesViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify products' images by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":10,
     "image": "product_image_url",
     "product":product_id
     }
     Use other functions by accessing this url:
     product/productImage/<productImage's_id>
     Format of data will be as the previous data format for GET function
     To Get All Product's Images for one product use this url:
     product/productImage/?product=<product_id>
    """

    def get_view_name(self):
        return _("Create/Modify Products Images")

    from .serializers import ProductImageSerializer
    serializer_class = ProductImageSerializer
    from .models import ProductImages
    permission_classes = [UnisealPermission]
    queryset = ProductImages.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']


class ProductVideoViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify products' videos by admin
        this endpoint allows GET,PUT,PATCH,DELETE functions
        permissions to this view is restricted as the following:
        - Only admin users can use all functions on this endpoint
        - Registered users are only allowed to use GET function
        Data will be retrieved in the following format for GET function:
        {
         "id":id,
         "video": "product_video_url",
         "product":product_id
         }
         Use other functions by accessing this url:
         product/productVideo/<productVideo's_id>
         Format of data will be as the previous data format for GET function
         To Get All Product's Videos for one product use this url:
         product/productVideo/?product=<product_id>
        """

    def get_view_name(self):
        return _("Create/Modify Products Videos")

    from .serializers import ProductVideoSerializer
    serializer_class = ProductVideoSerializer
    from .models import ProductVideos
    permission_classes = [UnisealPermission]
    queryset = ProductVideos.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']


class SimilarProductViewSet(viewsets.ModelViewSet):
    """API endpoint to allow the admin to link or unlink similar products together
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":9,
     "original_product": product_id,
     "similar_product":product_id
     }
     Use other functions by accessing this url:
     product/similarProducts/<similar_products's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Link/Unlink Similar Products")

    from .serializers import SimilarProductSerializer
    serializer_class = SimilarProductSerializer
    from .models import SimilarProduct
    permission_classes = [UnisealPermission]
    queryset = SimilarProduct.objects.all()


class FetchProductsByCategoryViewSet(generics.ListAPIView):
    """API endpoint to allow the admin to link or unlink similar products together
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":9,
     "original_product": product_id,
     "similar_product":product_id
     }
     Use other functions by accessing this url:
     product/similarProducts/<similar_products's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Fetch Products By Category")

    from .serializers import ProductSerializer
    serializer_class = ProductSerializer

    permission_classes = [UnisealPermission]

    from .models import Product
    queryset = Product.objects.all()

    # original get_queryset
    def get_queryset(self):
        from .models import Product
        # returning default result if anything goes wrong
        queryset = Product.objects.all()
        # category = self.request.query_params.get('category_id')
        category = self.kwargs['category_id']
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset
    # def get_queryset(self):
    #     # from itertools import chain
    #     from product.models import Product
    #     querysets = list()
    #     print(self.request.GET)
    #     print(self.request.query_params)
    #     if len(self.request.GET) != 0 :
    #         params = str(self.request.GET['category_id']).split(",")
    #         for param in params:
    #             listItems = Product.objects.filter(category__id=param)
    #             querysets += listItems
    #     else:
    #         queryset = Product.objects.all()
    #         querysets += queryset
    #
    #     # for product in resulting_list:
    #     #     print(product.product_file)
    #     # returning default result if anything goes wrong
    #     # category = self.request.query_params.get('category_id')
    #     # category = self.kwargs['category_id']
    #     # 00
    #     return querysets


# Views for product

from django.contrib.auth.decorators import login_required
@login_required(login_url='login')
def all_products(request):
    from product.models import Product
    all_products = Product.objects.all().order_by("id")
    paginator = Paginator(all_products, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        products = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        products = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        products = paginator.page(paginator.num_pages)
        page = paginator.num_pages



    return render(request, 'product/all_products.html',
                  {
                      'title': _('All Products'),
                      'all_products': 'active',
                      'all_products_data': products,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )


@login_required(login_url='login')
def add_products(request):
    from .forms import ProductForm
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save()
            product.slug = slugify(rand_slug())
            product.save()
            product_name = form.cleaned_data.get('name')

        else:
            print('there was an error dude!')
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
            # for msg in form.error_messages:
            #     messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = ProductForm()
    context = {
        'title': _('Add Products'),
        'add_products': 'active',
        'all_products': all_products,
        'form':form,
        # 'all_categories': all_categories,
        # 'all_suppliers': all_suppliers,
    }
    return render(request, 'product/add_products.html', context)

@login_required(login_url='login')
def delete_products(request):
    from product.models import Product
    all_products = Product.objects.all().order_by('id')
    paginator = Paginator(all_products, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        products = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        products = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        products = paginator.page(paginator.num_pages)
        page = paginator.num_pages




    context = {
        'title': _('Delete Products'),
        'delete_products': 'active',
        'all_products': all_products,
        'all_products_data': products,
        'page_range': paginator.page_range,
        'num_pages': paginator.num_pages,
        'current_page': page
    }
    return render(request, 'product/delete_products.html', context)

@login_required(login_url='login')
def edit_product(request,slug):
    from product.models import Product
    from .forms import ProductForm,ProductImagesForm
    all_products = Product.objects.all()
    # fetch the object related to passed id
    obj = get_object_or_404(Product, slug=slug)

    # pass the object as instance in form
    product_form = ProductForm(request.POST or None, instance=obj)
    product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if product_form.is_valid()  :
        product_form.save()
        product_image_form.save()
    context = {
        'title': _('Edit Products'),
        'edit_products': 'active',
        'all_products': all_products,
        'product_form':product_form,
        'product' : obj,
        'product_image_form':product_image_form
    }
    return render(request, 'product/edit_product.html', context)

@login_required(login_url='login')
def edit_products(request):
    from product.models import Product
    all_products = Product.objects.all().order_by("id")
    paginator = Paginator(all_products, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        products = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        products = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        products = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'product/edit_products.html',
                  {
                      'title': _('Edit Products'),
                      'edit_products': 'active',
                      'all_products_data': products,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def product_details(request,slug):
    from product.models import Product,ProductImages
    # from .forms import ProductForm
    # all_products = Product.objects.all().order_by("id")
    # paginator = Paginator(all_products, 5)
    # fetch the object related to passed id
    product = get_object_or_404(Product, slug=slug)
    productImages = ProductImages.objects.filter(product__slug=slug)
    pureImages = list()
    if productImages :
        pureImages.append(product.image.url)
        for image in productImages:
            pureImages.append(image.image.url)



    if request.method == "GET":
        if productImages :
            print("its noot empty yo!")
            print(product.image.url)
        else:
            print("its emmpty yoooo!")



    return render(request, 'product/product_detail.html',
                  {
                      'title': _('Product Details'),
                      'all_products': 'active',
                      'product_data': product,
                      'product_images':pureImages,
                      'product_original_image':product.image.url


                  }
                  )
@login_required(login_url='login')
def product_images(request,slug):
    from product.models import Product,ProductImages
    from .forms import ProductImagesForm
    # all_products = Product.objects.all().order_by("id")
    # paginator = Paginator(all_products, 5)
    # fetch the object related to passed id
    product = get_object_or_404(Product, slug=slug)
    productImages = ProductImages.objects.filter(product__slug=slug)
    pureImages = list()
    if productImages :
        pureImages.append(product.image.url)
        for image in productImages:
            pureImages.append(image.image.url)

    if request.method == 'POST':
        form = ProductImagesForm(request.POST)
        if form.is_valid():
            form.save()
            # country_name = form.cleaned_data.get('name')
            # messages.success(request, f"New Product Image Added: {country_name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = ProductImagesForm()



    return render(request, 'product/product_images.html',
                  {
                      'title': _('Product Images'),
                      'all_products': 'active',
                      'product_data': product,
                      'product_images':pureImages,
                      'product_original_image':product.image.url,
                      'form':form



                  }
                  )
def confirm_delete(request,id):
    from product.models import Product
    obj = get_object_or_404(Product, id=id)
    try:
        obj.delete()
        messages.success(request, f"Product {obj.name} deleted successfully")
    except:
        messages.error(request, f"Product {obj.name} was not deleted , please try again!")


    return redirect('deleteProducts')