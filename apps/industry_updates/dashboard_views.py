# from django.contrib import messages
# from django.contrib.admin.views.decorators import staff_member_required
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.shortcuts import render, get_object_or_404, redirect
# from django.template.defaultfilters import slugify
# from django.utils.translation import gettext_lazy as _
#
# from Util.utils import rand_slug
# from .models import IndustryUpdates
#
# updates = IndustryUpdates.objects.all().order_by('-id')
# @staff_member_required(login_url='login')
# def all_updates(request):
#     paginator = Paginator(updates, 5)
#
#     if request.GET.get('page'):
#         # Grab the current page from query parameter
#         page = int(request.GET.get('page'))
#     else:
#         page = None
#
#     try:
#         # Create a page object for the current page.
#         updates_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         # If the query parameter is empty then grab the first page.
#         updates_paginator = paginator.page(1)
#         page = 1
#     except EmptyPage:
#         # If the query parameter is greater than num_pages then grab the last page.
#         updates_paginator = paginator.page(paginator.num_pages)
#         page = paginator.num_pages
#
#     return render(request, 'industry_updates/all_updates.html',
#                   {
#                       'title': _('All Industry Updates'),
#                       'all_updates': 'active',
#                       'industry_updates':'active',
#                       'all_updates_data': updates_paginator,
#                       'page_range': paginator.page_range,
#                       'num_pages': paginator.num_pages,
#                       'current_page': page
#                   }
#                   )
#
# @staff_member_required(login_url='login')
# def add_updates(request):
#     from .forms import IndustryUpdatesForm
#     if request.method == 'POST':
#         form = IndustryUpdatesForm(request.POST,request.FILES)
#         if form.is_valid():
#             update_form = form.save(commit=False)
#             update_form.slug = slugify(rand_slug())
#             update_form.save()
#             link = form.cleaned_data.get('link')
#             messages.success(request, f"New Industry Updates Added: {link}")
#         else:
#             for field, items in form.errors.items():
#                 for item in items:
#                     messages.error(request, '{}: {}'.format(field, item))
#     else:
#         form = IndustryUpdatesForm()
#
#     context = {
#         'title': _('Add Industry Updates'),
#         'add_updates': 'active',
#         'form': form,
#         'industry_updates': 'active',
#     }
#     return render(request, 'industry_updates/add_updates.html', context)
# @staff_member_required(login_url='login')
# def delete_updates(request):
#     paginator = Paginator(updates, 5)
#
#     if request.GET.get('page'):
#         # Grab the current page from query parameter
#         page = int(request.GET.get('page'))
#     else:
#         page = None
#
#     try:
#         # Create a page object for the current page.
#         updates_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         # If the query parameter is empty then grab the first page.
#         updates_paginator = paginator.page(1)
#         page = 1
#     except EmptyPage:
#         # If the query parameter is greater than num_pages then grab the last page.
#         updates_paginator = paginator.page(paginator.num_pages)
#         page = paginator.num_pages
#
#     return render(request, 'industry_updates/delete_updates.html',
#                   {
#                       'title': _('Delete Industry Updates'),
#                       'industry_updates': 'active',
#                       'delete_updates': 'active',
#                       'all_updates_data': updates_paginator,
#                       'page_range': paginator.page_range,
#                       'num_pages': paginator.num_pages,
#                       'current_page': page
#                   }
#                   )
# @staff_member_required(login_url='login')
# def edit_updates(request):
#     paginator = Paginator(updates, 5)
#
#     if request.GET.get('page'):
#         # Grab the current page from query parameter
#         page = int(request.GET.get('page'))
#     else:
#         page = None
#
#     try:
#         # Create a page object for the current page.
#         updates_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         # If the query parameter is empty then grab the first page.
#         updates_paginator = paginator.page(1)
#         page = 1
#     except EmptyPage:
#         # If the query parameter is greater than num_pages then grab the last page.
#         updates_paginator = paginator.page(paginator.num_pages)
#         page = paginator.num_pages
#
#     return render(request, 'industry_updates/edit_updates.html',
#                   {
#                       'title': _('Edit Industry Updates'),
#                       'edit_updates': 'active',
#                       'industry_updates': 'active',
#                       'all_updates_data': updates_paginator,
#                       'page_range': paginator.page_range,
#                       'num_pages': paginator.num_pages,
#                       'current_page': page
#                   }
#                   )
# @staff_member_required(login_url='login')
# def edit_update(request,slug):
#     from .models import IndustryUpdates
#     from .forms import IndustryUpdatesForm
#     # fetch the object related to passed id
#     obj = get_object_or_404(IndustryUpdates, slug=slug)
#
#     # pass the object as instance in form
#     update_form = IndustryUpdatesForm(request.POST or None, instance=obj)
#     # product_image_form = ProductImagesForm(request.POST or None, instance=obj)
#
#     # save the data from the form and
#     # redirect to detail_view
#
#     if update_form.is_valid()  :
#         if request.FILES:
#             updates = update_form.save()
#             updates.image = request.FILES['image']
#             updates.save()
#         update_form.save()
#         link =  update_form.cleaned_data.get('link')
#         messages.success(request, f"Industry Update: {link} Updated")
#     else:
#         for field, items in update_form.errors.items():
#             for item in items:
#                 messages.error(request, '{}: {}'.format(field, item))
#
#     context = {
#         'title': _('Edit Industry Update'),
#         'edit_updates': 'active',
#         'update_form':update_form,
#         'update' : obj,
#         'industry_updates': 'active',
#     }
#     return render(request, 'industry_updates/edit_update.html', context)
# @staff_member_required(login_url='login')
# def confirm_delete(request,id):
#     from .models import IndustryUpdates
#     obj = get_object_or_404(IndustryUpdates, id=id)
#     try:
#         obj.delete()
#         messages.success(request, f"Industry Update: {obj.link} deleted successfully")
#     except:
#         messages.error(request, f"Industry Update: {obj.link} was not deleted , please try again!")
#
#
#     return redirect('deleteUpdates')
