from django.shortcuts import render
from django.utils.translation import gettext_lazy  as _

# Create your views here.
def error_404(request, exception):
    context = {
        'title': _('Page Not Found')
    }

    return render(request, 'handle_errors/404.html',context,status=400)

def error_500(request, *args, **argv):
    context = {
        'title':_('Internal Error 500')
    }

    return render(request, 'handle_errors/500.html',context,status=500)