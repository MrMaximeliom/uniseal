#TODO: add dashboard views for approvals
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic import ListView
from Util.search_form_strings import (CLEAR_SEARCH_TIP,SEARCH_APPROVALS_TIP ,
    APPROVAL_NOT_FOUND, ALL_APPROVALS_TITLE,
    EDIT_APPROVAL_TITLE , ADD_APPROVALS_TITLE,EDIT_APPROVALS_TITLE)
from Util.utils import delete_temp_folder, SearchMan, ReportMan, rand_slug
from .models import Approval,ApprovalImage
from .forms import ApprovalForm,ApprovalImagesForm
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView,UpdateView
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView



class ApprovalFormView(FormView):
    template_name = 'approvals/add_approvals.html'
    form_class = ApprovalForm
    success_url = 'addApprovals'

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        form.save()
        messages.success(self.request, f"Approval {name} Added Successfully")
        return super().form_valid(form)

    extra_context = {
        'approvals': 'active',
        'add_approvals': 'active',
        'title':ADD_APPROVALS_TITLE
    }


class ApprovalsListView(ListView):
    model = Approval
    template_name = "approvals/all_approvals.html"
    active_flag = 'all_approvals'
    searchManObj = SearchMan("Approval")
    search_result = None
    report_man = ReportMan()
    title = ALL_APPROVALS_TITLE


    def get_queryset(self):
        return Approval.objects.all().order_by('-id')

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            self.search_result = Approval.objects.all().filter(
                name=search_message).order_by('-id')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Approval Name')
            self.searchManObj.setSearchError(False)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.POST.get('clear') == 'clear':
            approvals = self.get_queryset()
            self.searchManObj.setPaginator(approvals)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            approvals = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            approvals = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            approvals = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'approvals': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'approvals_list': approvals,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_approvals_tip': SEARCH_APPROVALS_TIP,
            'current_page': page,
            'title':self.title
        }
        return super().get(request)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session:
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            approvals = Approval.objects.all().order_by('-id')
            self.searchManObj.setPaginator(approvals)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            approvals = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            approvals = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            approvals = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'approvals': 'active',
            self.active_flag: 'active',

            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'approvals_list': approvals,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_approvals_tip': SEARCH_APPROVALS_TIP,
            'not_found':APPROVAL_NOT_FOUND,
            'current_page': page,
            'title': self.title
        }
        return super().get(request)

class ApprovalDetailView(DetailView):
    model = Approval
    template_name = "approvals/approval_details.html"
    pureImages = list()
    def get(self, request, *args, **kwargs):
        self.pureImages = list()
        approvalImages = ApprovalImage.objects.filter(approval=self.get_object())
        for image in approvalImages:
                self.pureImages.append(image.image.url)
        self.extra_context.update({
          'object_images':self.pureImages
        })
        return super().get(request)
    extra_context = {
        'object_images':pureImages,
        'approvals':'active',
        'all_approvals':'active'
    }

@staff_member_required(login_url='login')
def approval_images(request, slug=None):
    from apps.approvals.models import Approval, ApprovalImage
    import os
    from .forms import ApprovalImagesForm
    allApprovals = Approval.objects.all()
    pureImages = {}
    context = {
        'title': _('Approval Images'),
        'approval_images_base': 'active',
        'allApprovals': allApprovals,
        'approvals': 'active',
    }
    if slug != None and request.method == 'GET':
        approval = get_object_or_404(Approval, slug=slug)
        productImages = ApprovalImage.objects.filter(approval__slug=slug)
        if productImages:
            for image in productImages:
                pureImages.update({image.image.url: image.image.url})
        context = {
            'title': _('Approval Images'),
            'approval_images_base': 'active',
            'approval_data': approval,
            'approval_images': pureImages,
            'allApprovals': allApprovals,
            'slug': slug
        }
        form = ApprovalImagesForm()
        context.update({"form": form})

    if request.method == 'POST' and 'search_product' in request.POST:
        if request.POST.get('search_options') != 'none':
            chosen_project = request.POST.get('search_options')
            return redirect('approvalImages', slug=chosen_project)
        else:
            messages.error(request, "Please choose approval from the list")

    if request.method == 'POST' and 'add_images' in request.POST:
        form = ApprovalImagesForm(request.POST, request.FILES)
        approval = get_object_or_404(Approval, slug=slug)
        selected_approval = Approval.objects.filter(slug=slug)
        files = request.FILES.getlist('image')
        form.approval = selected_approval
        if form.is_valid():
            if len(files) == 1:
                updated_approval = form.save(commit=False)
                updated_approval.image = request.FILES['image']
                # updated_project.project = selected_project.id
                updated_approval.slug = slugify(rand_slug())
                # updated_project.save()
                approval_name = approval.name
                messages.success(request, f"New image Added for: {approval_name}")

            else:
                for f in files:
                    ApprovalImage.objects.create(approval=approval, image=f)
                approval_name = approval.name
                messages.success(request, f"New images Added for: {approval_name}")
            return redirect('approvalImages', slug=slug)
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

    if request.method == 'POST' and 'confirm_changes' in request.POST:
        approval_instances = ApprovalImage.objects.filter(approval__slug=slug)
        deleted_images = request.POST.get('posted_deleted_images')

        current_approval = Approval.objects.get(slug=slug)

        if deleted_images != 'none':
            for instance in approval_instances:
                for image in deleted_images.split(','):
                    if instance.image.url == image:
                        deleted_image_path = os.path.dirname(os.path.abspath('unisealAPI')) + image
                        deleted_record = ApprovalImage.objects.get(id=instance.id)
                        deleted_record.delete()
                        if os.path.exists(deleted_image_path):
                            os.remove(deleted_image_path)

        messages.success(request, f"Approval {current_approval.name} was successfully updated!")
        return redirect('approvalImages', slug=slug)

    return render(request, 'approvals/approval_images.html',
                  context

                  )



class ApprovalUpdateView(UpdateView):
    model = Approval
    success_url = reverse_lazy('editApprovals')
    template_name = "approvals/edit_approval.html"



    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Approval Updated Successfully")
        return super().form_valid(form)
    fields = "__all__"
    extra_context = {
        'approvals': 'active',
        'edit_approvals': 'active',
        'title':EDIT_APPROVALS_TITLE,
        'clear_search_tip': CLEAR_SEARCH_TIP,
        'search_approvals_tip': SEARCH_APPROVALS_TIP,

    }


def confirm_delete(request, slug):
    from .models import Approval
    obj = get_object_or_404(Approval, slug=slug)
    try:
        obj.delete()
        messages.success(request, f"Approval {obj.name} deleted successfully")
    except:
        messages.error(request, f"Approval {obj.name} was not deleted , please try again!")
    return redirect('deleteApprovals')
