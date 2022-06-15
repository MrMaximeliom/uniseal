from django.http import HttpResponse


class EnablePartialUpdateMixin:
    """Enable partial updates

    Override partial kwargs in UpdateModelMixin class
    https://github.com/encode/django-rest-framework/blob/91916a4db14cd6a06aca13fb9a46fc667f6c0682/rest_framework/mixins.py#L64
    """

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


import datetime
from django.core.validators import MaxValueValidator
import string
import random


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))


SMS_USERNAME = 'uniseal'
SMS_PASSWORD = '823178'


def check_string_search_phrase(search_phrase):
    import re
    temp_holder = search_phrase
    special_char = re.findall(r'\W', temp_holder.replace(" ", ""))
    # returns true if search_phrase contains special chars and returns search_phrase without leading spaces
    return len(special_char) > 0, search_phrase.strip()


# TODO add logic to this function to use it later in the search functionality

def check_phone_number(phone):
    import re
    default_regex = r'^9\d{8}$|^1\d{8}$'
    another_regex = r'^09\d{8}$|^01\d{8}$'
    if re.findall(default_regex, phone):
        return True, re.findall(default_regex, phone)[0]
    elif re.findall(another_regex, phone):
        return True, re.findall(another_regex, phone)[0][1:]
    else:
        return False, ''


class ReportMan:
    filePath = ''
    fileName = ''

    # tempDir = ''
    def setFilePath(self, file_path):
        self.filePath = file_path

    def setFileName(self, file_name):
        self.fileName = file_name

    def getFilePath(self):
        return self.filePath

    def getFileName(self):
        return self.fileName
    # def setTempDir(self,dir_name):
    #     self.tempDir = dir_name
    # def getTempDir(self):
    #     return self.tempDir


class SearchMan:
    search_error = False
    queryset = None
    paginator = None

    def __init__(self, model):
        from django.core.paginator import Paginator
        from django.db.models import Count
        if model == "User":
            from apps.accounts.models import User
            users = User.objects.all().order_by("id")
            self.set_querySet(users)
            self.paginator = Paginator(users, 5)
        if model == "Product":
            from apps.product.models import Product
            products = Product.objects.all().order_by("id")
            self.set_querySet(products)
            self.paginator = Paginator(products, 5)
        if model == "Supplier":
            from apps.supplier.models import Supplier
            suppliers = Supplier.objects.all().order_by("id")
            self.set_querySet(suppliers)
            self.paginator = Paginator(suppliers, 5)
        if model == "Project":
            from apps.project.models import Project
            projects = Project.objects.all().order_by("id")
            self.set_querySet(projects)
            self.paginator = Paginator(projects, 5)
        if model == "Application":
            from apps.project.models import Application
            applications = Application.objects.annotate(num_projects=Count('project')).order_by('-num_projects')
            self.set_querySet(applications)
            self.paginator = Paginator(applications, 5)
        if model == "Category":
            from apps.category.models import Category
            categories = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')
            self.set_querySet(categories)
            self.paginator = Paginator(categories, 5)
        if model == "Country":
            from apps.address.models import Country
            countries = Country.objects.all().order_by('id')
            self.set_querySet(countries)
            self.paginator = Paginator(countries, 5)
        if model == "State":
            from apps.address.models import State
            states = State.objects.annotate(num_cities=Count('country')).order_by('-num_cities')
            self.set_querySet(states)
            self.paginator = Paginator(states, 5)
        if model == "City":
            from apps.address.models import City
            cities = City.objects.annotate(num_areas=Count('area')).order_by('-num_areas')
            self.set_querySet(cities)
            self.paginator = Paginator(cities, 5)
        if model == "Area":
            from apps.address.models import Area
            areas = Area.objects.all().order_by('id')
            self.set_querySet(areas)
            self.paginator = Paginator(areas, 5)
        if model == "Selling Point":
            from apps.sellingPoint.models import SellingPoint
            selling = SellingPoint.objects.all().order_by('id')
            self.set_querySet(selling)
            self.paginator = Paginator(selling, 5)
        if model == "Notifications":
            from apps.notifications.models import Notifications
            notifications = Notifications.objects.all().order_by('id')
            self.set_querySet(notifications)
            self.paginator = Paginator(notifications, 60)
        if model == "ProductVideos":
            from apps.application_videos.models import ProductApplicationVideos
            videos = ProductApplicationVideos.objects.all().order_by('id')
            self.set_querySet(videos)
            self.paginator = Paginator(videos, 5)
        if model == "Order":
            from apps.orders.models import Order
            orders = Order.objects.all().order_by('id')
            self.set_querySet(orders)
            self.paginator = Paginator(orders, 5)
        if model == "JobType":
            from apps.jop_type.models import JopType
            job_types = JopType.objects.annotate(num_users=Count('user')).order_by('id')
            self.set_querySet(job_types)
            self.paginator = Paginator(job_types, 5)
        if model == "Offer":
            from apps.offer.models import Offer
            offers = Offer.objects.all().order_by('id')
            self.set_querySet(offers)
            self.paginator = Paginator(offers, 5)
        if model == "Slider":
            from apps.slider.models import Slider
            sliders = Slider.objects.all().order_by('id')
            self.set_querySet(sliders)
            self.paginator = Paginator(sliders, 5)
        if model == "Request":
            from apps.request_permissions.models import RequestAccess
            requests = RequestAccess.objects.all().order_by('id')
            self.set_querySet(requests)
            self.paginator = Paginator(requests, 5)
        if model == "ManageProducts":
            from apps.admin_panel.models import ManageProducts
            manage_products = ManageProducts.objects.all().order_by('id')
            self.set_querySet(manage_products)
            self.paginator = Paginator(manage_products, 5)
        if model == "ManageProductsPage":
            from apps.admin_panel.models import ManageProductsPage
            manage_products_page = ManageProductsPage.objects.all().order_by('id')
            self.set_querySet(manage_products_page)
            self.paginator = Paginator(manage_products_page, 5)
        if model == "ManageProjects":
            from apps.admin_panel.models import ManageProjects
            manage_projects_page = ManageProjects.objects.all().order_by('id')
            self.set_querySet(manage_projects_page)
            self.paginator = Paginator(manage_projects_page, 5)
        if model == "ManageSolutions":
            from apps.admin_panel.models import ManageSolution
            manage_solutions_page = ManageSolution.objects.all().order_by('id')
            self.set_querySet(manage_solutions_page)
            self.paginator = Paginator(manage_solutions_page, 5)
        if model == "Brochures":
            from apps.brochures.models import Brochures
            brochures = Brochures.objects.all().order_by('id')
            self.set_querySet(brochures)
            self.paginator = Paginator(brochures, 5)
        if model == "IndustryUpdates":
            from apps.industry_updates.models import IndustryUpdates
            updates = IndustryUpdates.objects.all().order_by('id')
            self.set_querySet(updates)
            self.paginator = Paginator(updates, 5)
        if model == "ManageBrochures":
            from apps.admin_panel.models import ManageBrochures
            manage_brochures_page = ManageBrochures.objects.all().order_by('id')
            self.set_querySet(manage_brochures_page)
            self.paginator = Paginator(manage_brochures_page, 5)
        if model == "ManageOrders":
            from apps.admin_panel.models import ManageCarts
            manage_orders_page = ManageCarts.objects.all().order_by('id')
            self.set_querySet(manage_orders_page)
            self.paginator = Paginator(manage_orders_page, 5)
        if model == "Approval":
            from apps.approvals.models import Approval
            approvals = Approval.objects.all().order_by('id')
            self.set_querySet(approvals)
            self.paginator = Paginator(approvals, 5)
        if model == "SMSNotification":
            from apps.sms_notifications.models import SMSNotification
            sms_notifications = SMSNotification.objects.all().order_by('id')
            self.set_querySet(sms_notifications)
            self.paginator = Paginator(sms_notifications, 5)
        if model == "SMSContacts":
            from apps.sms_notifications.models import SMSContacts
            sms_contacts = SMSContacts.objects.all().order_by('id')
            self.set_querySet(sms_contacts)
            self.paginator = Paginator(sms_contacts, 5)
        if model == "SMSGroups":
            from apps.sms_notifications.models import SMSGroups
            sms_groups = SMSGroups.objects.all().order_by('id')
            self.set_querySet(sms_groups)
            self.paginator = Paginator(sms_groups, 5)
        if model == "SMSGroupMessages":
            from apps.sms_notifications.models import SMSGroupMessages
            sms_group_messages= SMSGroupMessages.objects.all().order_by('id')
            self.set_querySet(sms_group_messages)
            self.paginator = Paginator(sms_group_messages, 5)


    def setPaginator(self, query, num_records=5):
        from django.core.paginator import Paginator
        self.paginator = Paginator(query, num_records)

    def getPaginator(self):
        return self.paginator

    search = False
    search_phrase = ''
    search_option = ''

    def setSearch(self, bool):
        self.search = bool

    def getSearch(self):
        return self.search

    def setSearchPhrase(self, phrase):
        self.search_phrase = phrase

    def getSearchPhrase(self):
        return self.search_phrase

    def setSearchOption(self, option):
        self.search_option = option

    def getSearchOption(self):
        return self.search_option

    def setSearchError(self, bool):
        self.search_error = bool

    def getSearchError(self):
        return self.search_error

    def set_querySet(self,queryset):
        self.queryset = queryset

    def get_queryset(self):
        return self.queryset


def createExelFile(report_name, headers, request=None, **kwargs):
    from django.contrib import messages
    import xlsxwriter, os
    from string import ascii_uppercase
    from datetime import date
    from datetime import datetime
    # get current day to link it to Excel file name
    today = date.today()
    # get current time to link it to Excel file name
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    path = os.path.dirname(os.path.abspath(__file__)) + "/Reports"
    if not os.path.isdir(path):
        os.mkdir(path)
    file_name = report_name + '_' + str(today) + '_' + str(current_time) + ".xlsx"
    complete_file_name = os.path.abspath(path) + "/" + file_name
    workBok = xlsxwriter.Workbook(complete_file_name, options={'remove_timezone': True})
    sheet = workBok.add_worksheet()
    AlphabetLetters = ''.join(c for c in ascii_uppercase)
    for c in range(len(headers)):
        sheet.write(f"{AlphabetLetters[c]}1", headers[c])
    x_position = -1
    for key, value in kwargs.items():
        x_position = x_position + 1
        for item in range(len(value)):
            sheet.write(item + 1, x_position, value[item])
    try:
        workBok.close()
        file_creation_status = True
        if request is not None:
            messages.success(request, f"Report Successfully Created ")
        return file_creation_status, str(complete_file_name), str(file_name)
    except:
        file_creation_status = False
    return file_creation_status, str(complete_file_name), str(file_name)

    # return workBok


def download_file(request, file_path, file_name):
    import mimetypes
    path = open(file_path, 'rb')
    # # Set the mime type
    mime_type, _ = mimetypes.guess_type(file_path)
    # # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % file_name
    # # Return the response value
    return response


def delete_temp_folder():
    import os.path
    myPath = os.path.dirname(os.path.abspath(__file__)) + "/Reports"
    for root, dirs, files in os.walk(myPath):
        for file in files:
            os.remove(os.path.join(root, file))


def random_order_id(letter_count, digit_count):
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    import datetime
    today = datetime.date.today()
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1)  # it converts the string to list.
    random.shuffle(sam_list)  # It uses a random.shuffle() function to shuffle the string.
    final_string = ''.join(sam_list)
    return "order-" + final_string + "-" + current_time + "-" + str(today)
