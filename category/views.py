from django.db.models import Count
from django.template.defaultfilters import slugify
from rest_framework import viewsets
from django.contrib import messages

from Util.permissions import  UnisealPermission

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from Util.utils import rand_slug


class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify categories' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id": 12,
     "name":"category_name",
     }
     Use other functions by accessing this url:
     category/<category's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Categories")

    from .serializers import CategorySerializer
    serializer_class = CategorySerializer
    from .models import Category
    permission_classes = [UnisealPermission]
    queryset = Category.objects.all()
#Views for dashboard
from category.models import Category
categories = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')

def all_categories(request):
    paginator = Paginator(categories, 5)

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        categories_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        categories_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        categories_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'category/all_categories.html',
                  {
                      'title': _('All Categories'),
                      'all_categories': 'active',
                      'all_categories_data': categories_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )


def add_categories(request):
    from .forms import CategoryForm
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form = form.save()
            form.slug = slugify(rand_slug())
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"New Category Added: {name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = CategoryForm()

    context = {
        'title': _('Add Categories'),
        'add_categories': 'active',
        'form': form,
    }
    return render(request, 'category/add_categories.html', context)

def delete_categories(request):
    paginator = Paginator(categories, 5)

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        categories_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        categories_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        categories_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'category/delete_categories.html',
                  {
                      'title': _('Delete Categories'),
                      'delete_categories': 'active',
                      'all_categories_data': categories_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

def edit_categories(request):
    paginator = Paginator(categories, 5)

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        categories_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        categories_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        categories_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'category/edit_categories.html',
                  {
                      'title': _('Edit Categories'),
                      'edit_categories': 'active',
                      'all_categories_data': categories_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

def edit_category(request,slug):
    from .models import Category
    from .forms import CategoryForm
    all_products = Category.objects.all()
    # fetch the object related to passed id
    obj = get_object_or_404(Category, slug=slug)

    # pass the object as instance in form
    category_form = CategoryForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if category_form.is_valid()  :
        category_form.save()
        name =  category_form.cleaned_data.get('name')
        messages.success(request, f"Category {name} Updated")
    else:
        for field, items in category_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Category'),
        'edit_categories': 'active',
        'category_form':category_form,
        'category' : obj,
    }
    return render(request, 'category/edit_category.html', context)

def confirm_delete(request,id):
    from category.models import Category
    obj = get_object_or_404(Category, id=id)
    try:
        obj.delete()
        messages.success(request, f"Category {obj.name} deleted successfully")
    except:
        messages.error(request, f"Category {obj.name} was not deleted , please try again!")


    return redirect('deleteCategories')