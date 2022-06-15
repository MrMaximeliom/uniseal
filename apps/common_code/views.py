from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView

from Util.utils import SearchMan

"""
ModelListView Class:
is a class used to list instances of a specified model,
it requires to define the following params:
- model (the model of the updated instance)
- template_name ( the path of the view that will be used)
- active_flag (this flag is used to add 'active' class to the current pages in sidebar) 
- main_active_flag (this flag is used to add 'active' class to the main master current pages in sidebar) 
- model_name (this variable is used to specify model name for SearchMan class) 
- no_records_admin (this variable is used to specify the message that appears 
                     if there are no records for the admin user) 
- no_records_monitor (this variable is used to specify the message that appears 
                     if there are no records for the monitor user) 
- add_tool_tip_text (specifies the text that appears while hovering the 'add' button)
- update_tool_tip_text (specifies the text that appears while hovering the 'update' button)
- title (specifies the page's title)
"""


class ModelListView(ListView):

    model = None
    template_name = None
    main_active_flag = None
    active_flag = None
    model_name = None
    no_records_admin = None
    no_records_monitor = None
    add_tool_tip_text = None
    update_tool_tip_text = None
    title = None
    searchManObj = SearchMan(model_name)

    # return default queryset used in this view
    def get_queryset(self):
        queryset = self.searchManObj.get_queryset()
        if queryset:
            return queryset
        return self.model.objects.all().order_by('-id')

    def get(self, request, *args, **kwargs):
        searchManObj = SearchMan(self.model_name)
        queryset = searchManObj.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'page' not in request.GET:
            instances = searchManObj.get_queryset()
            print(searchManObj.get_queryset())
            searchManObj.setPaginator(instances)
            searchManObj.setSearch(False)
            self.searchManObj.set_querySet(instances)
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
            "no_records_admin": self.no_records_admin,
            "no_records_monitor": self.no_records_monitor,
            "add_tool_tip_text": self.add_tool_tip_text,
            "update_tool_tip_text": self.update_tool_tip_text,
            "instances_count": len(self.searchManObj.get_queryset()),
            'current_page': page,
            'title': self.title
        }
        return super().get(request)


class BaseListView(ListView):
    model = None
    template_name = None
    main_active_flag = None
    active_flag = None
    model_name = None
    no_records_admin = None
    no_records_monitor = None
    add_tool_tip_text = None
    update_tool_tip_text = None
    title = None
    searchManObj = SearchMan(model_name)

    # return default queryset used in this view
    def get_queryset(self):
        return self.model.objects.all().order_by('-id')






"""
AddModelView Class:
is a class used to add instances of a specified model,
it requires to define the following params:
- model (the model to add new instances)
- template_name ( the path of the view that will be used)
- active_flag (this flag is used to add 'active' class to the current pages in sidebar) 
- reference_field_name (this field used to reference the field that will be used in success/error messages) 
- main_active_flag (this flag is used to add 'active' class to the main master current pages in sidebar)
- title (specifies the page's title)
"""


class AddModelView(CreateView):
    model = None
    fields = None
    template_name = None
    active_flag = None
    reference_field_name = None
    main_active_flag = None
    title = None
    success_url = None

    def form_invalid(self, form):
        for field, items in form.errors.items():
            for item in items:
                print('{}: {}'.format(field, item))
        instance_name = form.cleaned_data[self.reference_field_name]
        messages.error(self.request, f"{self.active_flag} <<{instance_name}>> did not added , please try again!")
        return super(AddModelView, self).form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        instance_name = form.cleaned_data[self.reference_field_name]
        self.object.added_by = self.request.user
        self.object.save()
        messages.success(self.request, f"{self.active_flag} <<{instance_name}>> added successfully")
        success_url = self.get_success_url()
        return redirect(success_url)

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            self.main_active_flag: "active",
            self.active_flag: "active",
            "title": self.title
        }
        return super(AddModelView, self).get(self)

    def post(self, request, *args, **kwargs):
        self.extra_context = {
            self.main_active_flag: "active",
            self.active_flag: "active",
            "title": self.title
        }
        return super(AddModelView, self).post(self)


"""
UpdateModelView Class:
is a class used to update instances of a specified model,
it requires to define the following params:
- model (the model of the updated instance)
- template_name ( the path of the view that will be used)
- active_flag (this flag is used to add 'active' class to the current pages in sidebar) 
- reference_field_name (this field used to reference the field that will be used in success/error messages) 
- main_active_flag (this flag is used to add 'active' class to the main master current pages in sidebar)
- title (specifies the page's title)
"""


class UpdateModelView(UpdateView):
    model = None
    fields = None
    template_name = None
    active_flag = None
    reference_field_name = None
    main_active_flag = None
    title = None
    success_url = None

    def form_invalid(self, form):
        for field, items in form.errors.items():
            for item in items:
                print('{}: {}'.format(field, item))
        instance_name = form.cleaned_data[self.reference_field_name]
        messages.error(self.request, f"{self.active_flag} <<{instance_name}>> did not updated , please try again!")
        return super(UpdateModelView, self).form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.last_modified_by = self.request.user
        self.object.save()
        instance_name = form.cleaned_data[self.reference_field_name]
        messages.success(self.request, f"{self.active_flag} <<{instance_name}>> updated successfully")
        success_url = self.get_success_url()
        return redirect(success_url)

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            self.main_active_flag: "active",
            self.active_flag: "active",
            "title": self.title,
        }
        return super(UpdateModelView, self).get(self)

    def post(self, request, *args, **kwargs):
        self.extra_context = {
            self.main_active_flag: "active",
            self.active_flag: "active",
            "title": self.title
        }
        return super(UpdateModelView, self).post(self)

class ModelDetailsView(DetailView):
    model = None
    main_active_flag = None
    active_flag = None
    title = None
    def get(self, request, *args, **kwargs):
        self.extra_context = {
            self.main_active_flag: "active",
            self.active_flag: "active",
            "title": self.title
        }
        return super(ModelDetailsView, self).get(self)

class ModelDeleteView(DeleteView):
    model = None
    active_flag = None
    model_name = None
    main_active_flag = None
    title = None
    success_url = None

    def form_invalid(self, form):
        for field, items in form.errors.items():
            for item in items:
                print('{}: {}'.format(field, item))
        messages.error(self.request, f"{self.model_name} <<{self.object}>> did not deleted , please try again!")
        return super(ModelDeleteView, self).form_invalid(form)

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, f"{self.model_name} <<{self.object}>> deleted successfully")
        return redirect(success_url)

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            self.main_active_flag: "active",
            self.active_flag: "active",
            "title": self.title,
        }
        return super(ModelDeleteView, self).get(self)

    def post(self, request, *args, **kwargs):
        print("in post method")
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)






