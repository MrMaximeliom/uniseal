from django.views.generic import ListView
from .models import JopType
from .forms import JobTypeForm
from django.views.generic.edit import FormView
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
class JopTypeFormView(FormView):
    template_name = 'jop_type/add_jop_types.html'
    form_class = JobTypeForm
    success_url = 'addJopTypes'
    def form_valid(self, form):
        form.save()
        messages.success(self.request,"Jop Type Added Successfully")
        return super().form_valid(form)
    extra_context = {
        'job': 'active',
        'add_job_types':'active'
    }

class JopTypeListView(ListView):
    model = JopType
    template_name = "jop_type/all_jop_types.html"
    # queryset =  JopType.objects.all()
    def get_queryset(self):
        return JopType.objects.annotate(num_users=Count('user')).order_by('-num_users')
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            jop_types = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            jop_types = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            jop_types = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'job':'active',
            'all_job_types':'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'current_page': page,
        }
        return super().get(request)
