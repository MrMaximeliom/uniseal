from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

# Dashboard Views
from .models import Brochures

brochures = Brochures.objects.all().order_by("id")
@staff_member_required(login_url='login')
def all_brochures(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(brochures, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        brochures_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        brochures_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        brochures_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'brochures/all_brochures.html',
                  {
                      'title': _('All Brochures'),
                      'all_brochures': 'active',
                      'brochures':'active',
                      'all_brochures_data': brochures_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )


@staff_member_required(login_url='login')
def add_brochures(request):
    from .forms import BrochuresForm
    if request.method == 'POST':
        form = BrochuresForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f"New Brochure Added: {title}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = BrochuresForm()


    context = {
        'title': _('Add Brochures'),
        'add_brochures': 'active',
        'form': form,
        'brochures': 'active',
    }
    return render(request, 'brochures/add_brochures.html', context)

@staff_member_required(login_url='login')
def delete_brochures(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(brochures, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        brochures_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        brochures_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        brochures_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'brochures/delete_brochures.html',
                  {
                      'title': _('Delete Brochures'),
                      'delete_brochures': 'active',
                      'all_brochures_data': brochures_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'brochures': 'active',
                  }
                  )


@staff_member_required(login_url='login')
def edit_brochures(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(brochures, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        brochures_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        brochures_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        brochures_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'brochures/edit_brochures.html',
                  {
                      'title': _('Edit Brochures'),
                      'edit_brochures': 'active',
                      'all_brochures_data': brochures_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'brochures': 'active',
                  }
                  )
@staff_member_required(login_url='login')
def edit_brochure(request,slug):
    from .models import Brochures
    from .forms import BrochuresForm

    obj = get_object_or_404(Brochures, slug=slug)

    # pass the object as instance in form
    brochure_form = BrochuresForm(request.POST or None, instance=obj)
    # save the data from the form and
    # redirect to detail_view
    if brochure_form.is_valid():
        if request.FILES:
            Brochures = brochure_form.save()
            Brochures.image = request.FILES['image']
            Brochures.save()
        brochure_form.save()
        point_name = brochure_form.cleaned_data.get('title')
        messages.success(request, f"Successfully Updated : {point_name} Data")
    else:
        for field, items in brochure_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Brochures'),
        'edit_brochures': 'active',
        'form': brochure_form,
        'brochure': obj,
        'brochures': 'active',

    }
    return render(request, 'brochures/edit_brochure.html', context)


def confirm_delete(request,id):
    from .models import Brochures
    obj = get_object_or_404(Brochures, id=id)
    try:
        obj.delete()
        messages.success(request, f"Brochure: {obj.title} deleted successfully")
    except:
        messages.error(request, f"Brochure: {obj.title} was not deleted , please try again!")


    return redirect('deleteBrochures')