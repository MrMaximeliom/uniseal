from django.shortcuts import render
from django.utils.translation import gettext as _
# Create your views here.
def dashboard(request):

    context = {
        'title':  _('Uniseal API Admin Dashboard'),
        'home' : 'active',

    }

    return render(request, 'dashboard/index.html', context)
