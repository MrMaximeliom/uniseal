from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

# Create your views here.
from Util.utils import rand_slug
# Views for dashboard
from slider.models import Slider

sliders = Slider.objects.all()
@staff_member_required(login_url='login')
def all_sliders(request):
    from .models import Slider
    all_sliders = Slider.objects.all().order_by("id")
    paginator = Paginator(all_sliders, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        sliders = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        sliders = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        sliders = paginator.page(paginator.num_pages)
        page = paginator.num_pages



    return render(request, 'slider/all_sliders.html',
                  {
                      'title': _('All Sliders'),
                      'sliders':'active',
                      'all_sliders': 'active',
                      'all_sliders_data': sliders,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@staff_member_required(login_url='login')
def add_sliders(request):
    from .forms import SliderForm
    if request.method == 'POST':
        form = SliderForm(request.POST,request.FILES)
        if form.is_valid():
            slider = form.save()
            slider.slug = slugify(rand_slug())
            slider.save()
            title = form.cleaned_data.get('title')
            if title != "":
                messages.success(request, f"New Slider Added: {title}")
            else:
                messages.success(request, f"New Slider Added")

        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = SliderForm()

    context = {
        'title': _('Add Sliders'),
        'add_sliders': 'active',
        'form': form,
        'sliders': 'active',
    }
    return render(request, 'slider/add_sliders.html', context)
@staff_member_required(login_url='login')
def delete_sliders(request):
    from .models import Slider
    all_sliders = Slider.objects.all().order_by("id")
    paginator = Paginator(all_sliders, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        sliders = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        sliders = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        sliders = paginator.page(paginator.num_pages)
        page = paginator.num_pages



    return render(request, 'slider/delete_sliders.html',
                  {
                      'title': _('Delete Sliders'),
                      'delete_sliders': 'active',
                      'sliders': 'active',
                      'all_sliders_data': sliders,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@staff_member_required(login_url='login')
def edit_sliders(request):
    from .models import Slider
    all_sliders = Slider.objects.all().order_by("id")
    paginator = Paginator(all_sliders, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        sliders = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        sliders = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        sliders = paginator.page(paginator.num_pages)
        page = paginator.num_pages



    return render(request, 'slider/edit_sliders.html',
                  {
                      'title': _('Edit Sliders'),
                      'edit_sliders': 'active',
                      'sliders': 'active',
                      'all_sliders_data': sliders,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@staff_member_required(login_url='login')
def edit_slider(request,slug):
    from .models import Slider
    from .forms import SliderForm
    all_sliders = Slider.objects.all()
    # fetch the object related to passed id
    obj = get_object_or_404(Slider, slug=slug)

    # pass the object as instance in form
    slider_form = SliderForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if slider_form.is_valid():
        if request.FILES:
            slider = slider_form.save()
            slider.image = request.FILES['image']
            slider.save()
            slider_title = slider_form.cleaned_data.get('title')
            # messages.success(request, f"Successfully Updated : {slider_title} Data")
        slider_form.save()
    else:
        for field, items in slider_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Sliders'),
        'edit_sliders': 'active',
        'all_sliders': all_sliders,
        'slider_form': slider_form,
        'slider': obj,
        'sliders': 'active',
    }
    return render(request, 'slider/edit_slider.html', context)
@staff_member_required(login_url='login')
def confirm_delete(request,id):
    from .models import Slider
    obj = get_object_or_404(Slider, id=id)
    try:
        obj.delete()
        messages.success(request, f"Slider {obj.link} deleted successfully")
    except:
        messages.error(request, f"Slider {obj.link} was not deleted , please try again!")


    return redirect('deleteSliders')
