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
    return len(special_char) > 0 , search_phrase.strip()
# TODO add logic to this function to use it later in the search functionality

def check_phone_number(phone):
    import re
    default_regex = r'^9\d{8}$|^1\d{8}$'
    another_regex = r'^09\d{8}$|^01\d{8}$'
    if re.findall(default_regex, phone):
        return True,re.findall(default_regex,phone)[0]
    elif re.findall(another_regex,phone):
        return True, re.findall(another_regex,phone)[0][1:]
    else:
        return False,''

class ReportMan:
    filePath = ''
    fileName = ''
    # tempDir = ''
    def setFilePath(self,file_path):
        self.filePath = file_path
    def setFileName(self,file_name):
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

    def __init__(self,model):
        from django.core.paginator import Paginator
        from django.db.models import Count
        if model == "User":
            from accounts.models import User
            users = User.objects.all().order_by("id")
            self.paginator = Paginator(users, 5)
        if model == "Product":
            from product.models import Product
            products = Product.objects.all().order_by("id")
            self.paginator = Paginator(products, 5)
        if model == "Supplier":
            from supplier.models import Supplier
            suppliers = Supplier.objects.all().order_by("id")
            self.paginator = Paginator(suppliers, 5)
        if model == "Project":
            from project.models import Project
            projects = Project.objects.all().order_by("id")
            self.paginator = Paginator(projects, 5)
        if model == "Application":
            from project.models import Application
            applications = Application.objects.annotate(num_projects=Count('project')).order_by('-num_projects')
            self.paginator = Paginator(applications, 5)
        if model == "Category":
            from category.models import Category
            categories = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')
            self.paginator = Paginator(categories, 5)
        if model == "Country":
            from address.models import Country
            countries = Country.objects.all().order_by('id')
            self.paginator = Paginator(countries, 5)
        if model == "State":
            from address.models import State
            states = State.objects.annotate(num_cities=Count('city')).order_by('-num_cities')
            self.paginator = Paginator(states, 5)
        if model == "City":
            from address.models import City
            cities = City.objects.annotate(num_areas=Count('area')).order_by('-num_areas')
            self.paginator = Paginator(cities, 5)
        if model == "Area":
            from address.models import Area
            areas = Area.objects.all().order_by('id')
            self.paginator = Paginator(areas, 5)
        if model == "Selling Point":
            from sellingPoint.models import SellingPoint
            selling = SellingPoint.objects.all().order_by('id')
            self.paginator = Paginator(selling, 5)
        if model == "Notifications":
            from notifications.models import Notifications
            notifications = Notifications.objects.all().order_by('id')
            self.paginator = Paginator(notifications, 5)
        if model == "ProductVideos":
            from application_videos.models import ProductApplicationVideos
            videos = ProductApplicationVideos.objects.all().order_by('id')
            self.paginator = Paginator(videos, 5)




    def setPaginator(self,query):
        from django.core.paginator import Paginator
        self.paginator = Paginator(query, 5)

    def getPaginator(self):
        return self.paginator
    search = False
    search_phrase = ''
    search_option = ''
    def setSearch(self,bool):
        self.search = bool
    def getSearch(self):
        return self.search
    def setSearchPhrase(self,phrase):
        self.search_phrase = phrase
    def getSearchPhrase(self):
        return  self.search_phrase
    def setSearchOption(self, option):
        self.search_option = option
    def getSearchOption(self):
        return self.search_option
    def setSearchError(self,bool):
        self.search_error=bool
    def getSearchError(self):
        return self.search_error

def createExelFile(report_name,headers,request=None,**kwargs):
    from django.contrib import messages
    import xlsxwriter , os
    from string import ascii_uppercase
    from datetime import date
    from datetime import datetime
    # get current day to link it to excel file name
    today = date.today()
    # get current time to link it to excel file name
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    path  = os.path.dirname(os.path.abspath(__file__)) + "/Reports"
    if not os.path.isdir(path):
        os.mkdir(path)
    file_name = report_name+'_'+str(today)+'_'+str(current_time)+".xlsx"
    complete_file_name = os.path.abspath(path)+"/"+file_name
    print("file name is ",file_name)
    print("complete file name is: ",complete_file_name)
    workBok = xlsxwriter.Workbook(complete_file_name,options={'remove_timezone': True})
    sheet = workBok.add_worksheet()
    AlphabetLetters = ''.join(c for c in ascii_uppercase)
    for c in range(len(headers)):
        sheet.write(f"{AlphabetLetters[c]}1",headers[c])
    x_position = -1
    for key, value in kwargs.items():
        x_position = x_position+1
        for item in range(len(value)):
            sheet.write(item + 1,  x_position, value[item])
    try:
        workBok.close()
        file_creation_status = True
        print("created")
        if request is not None:
            messages.success(request, f"Report Successfully Created ")

        return file_creation_status,str(complete_file_name),str(file_name)

    except:
        file_creation_status = False
    return file_creation_status,str(complete_file_name),str(file_name)


    # return workBok


def download_file(request,file_path,file_name):
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
