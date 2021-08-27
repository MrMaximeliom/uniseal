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
    import tempfile
    filePath = ''
    fileName = ''
    tempDir = ''
    def setFilePath(self,file_path):
        self.filePath = file_path
    def setFileName(self,file_name):
        self.fileName = file_name
    def getFilePath(self):
        return self.filePath
    def getFileName(self):
        return self.fileName
    def setTempDir(self,dir_name):
        self.tempDir = dir_name
    def getTempDir(self):
        return self.tempDir
class SearchMan:
    search_error = False

    def __init__(self,model):
        from django.core.paginator import Paginator
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

def createExelFile(report_man,report_name,headers,**kwargs):
    import xlsxwriter , os
    from string import ascii_uppercase
    from datetime import date
    from datetime import datetime
    # get current day to link it to excel file name
    today = date.today()
    # get current time to link it to excel file name
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # getting root file system directory
    rootDir = os.path.abspath('.').split(os.path.sep)[0] + os.path.sep
    # getting desktop directory
    desktop_dir = os.path.expanduser("~/Desktop")
    # creating Reports directory
    reports_dir = "Reports"
    # create reports directory in desktop directory
    # path = os.path.join( desktop_dir, reports_dir)
    # check if it's not created , create it now otherwise ignore
    # if os.path.isfile(path):
    #     os.mkdir(path)
    # complete_file_name = os.path.abspath(path)+"/"+
    # create temp directory and add excel file in it
    import tempfile , shutil
    # create temp directory
    import os
    if not os.path.exists(report_man.getTempDir()):
        report_man.setTempDir(tempfile.mkdtemp())
    tempDir = report_man.tempDir
    # shutil.rmtree(tempDir)
    # path = os.path.join(tempDir, reports_dir)
    path = tempDir
    # if os.path.isfile(path):
    #     os.mkdir(path) print("here in supplier")
    # else:
    #     os.mkdir(path)
    file_name = report_name+'_'+str(today)+'_'+str(current_time)+".xlsx"
    complete_file_name = os.path.abspath(path)+"/"+file_name
    print("file name is ",file_name)
    print("complete file name is: ",complete_file_name)
    # os.path.join(op.name, dd)


    workBok = xlsxwriter.Workbook(complete_file_name,options={'remove_timezone': True})
    sheet = workBok.add_worksheet()
    AlphabetLetters = ''.join(c for c in ascii_uppercase)
    # create the headers first
    # headers structure should look like this
    '''
    headers = {
    0:"username",
    1:"Organization",
    }
    '''
    for c in range(len(headers)):
        # print(f"{AlphabetLetters[c]}1", headers[c])
        sheet.write(f"{AlphabetLetters[c]}1",headers[c])
    # add data to headers , remember that xlsxwriter package renders cells as y,x axis not x,y axis
    x_position = -1
    for key, value in kwargs.items():
        x_position = x_position+1
        for item in range(len(value)):
            sheet.write(item + 1,  x_position, value[item])
    # file_creation_status = True
    try:
        workBok.close()
        file_creation_status = True
        print("created")
        return file_creation_status,complete_file_name,file_name

    except:
        file_creation_status = False
    return file_creation_status,complete_file_name,file_name


    # return workBok


def download_file(request,file_path,file_name):
    import os,mimetypes
    path = open(file_path, 'rb')
    # # Set the mime type
    mime_type, _ = mimetypes.guess_type(file_path)
    # # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % file_name
    # # Return the response value
    return response

def delete_temp_folder(tempDir):
    import os , shutil
    # shutil.rmtree(tempDir)
    if  os.path.exists(tempDir):
        print('temp directory deleted')
        shutil.rmtree(tempDir)
