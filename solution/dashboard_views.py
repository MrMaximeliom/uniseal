from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

# Views for dashboard
from solution.models import Solution

# Create your views here.
solutions = Solution.objects.all()
@login_required(login_url='login')
def all_solutions(request):
    # from solution.models import Solution
    # all_solutions = Solution.objects.all()
    context = {
        'title': _('All Solutions'),
        'all_solutions': 'active',
        'all_solutions_data': solutions,
        'solutions':'active',
    }
    return render(request, 'solution/all_solutions.html', context)
@login_required(login_url='login')
def add_solutions(request):

    context = {
        'title': _('Add Solutions'),
        'add_solutions': 'active',
        'all_solutions': solutions,
        'solutions': 'active',
    }
    return render(request, 'solution/add_solutions.html', context)
@login_required(login_url='login')
def delete_solutions(request):

    context = {
        'title': _('Delete Solutions'),
        'delete_solutions': 'active',
        'all_solutions': solutions,
        'solutions': 'active',
    }
    return render(request, 'solution/delete_solutions.html', context)
@login_required(login_url='login')
def edit_solutions(request):
    context = {
        'title': _('Edit Solutions'),
        'edit_solutions': 'active',
        'all_solutions': solutions,
        'solutions': 'active',
    }
    return render(request, 'solution/edit_solutions.html', context)

