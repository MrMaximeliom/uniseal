from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import gettext_lazy as _

# Create your views here.

def all_sms(request):
    from sms_notifications.models import SMSNotification
    all_sms = SMSNotification.objects.all().order_by("id")
    paginator = Paginator(all_sms, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        sms = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        sms = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        sms = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sms_notifications/all_sms.html',
                  {
                      'title': _('All SMS'),
                      'all_sms_notifications': 'active',
                      'all_sms_data': sms,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
def send_sms(request):
    from sms_notifications.models import SMSNotification
    from sms_notifications.models import SMSGroups
    from sms_notifications.models import SMSContacts
    all_sms = SMSNotification.objects.all()
    all_sms_groups = SMSGroups.objects.all()
    all_sms_contacts =SMSContacts.objects.all()
    context = {
        'title': _('Add Products'),
        'send_sms': 'active',
        'all_sms': all_sms,
        'all_sms_groups': all_sms_groups,
        'all_sms_contacts':all_sms_contacts,
    }
    return render(request, 'sms_notifications/send_sms.html', context)
def delete_sms(request):
    from sms_notifications.models import SMSNotification
    all_sms = SMSNotification.objects.all()
    context = {
        'title': _('Delete SMS'),
        'delete_products': 'active',
        'all_products': all_sms,
    }
    return render(request, 'sms_notifications/delete_sms.html', context)

