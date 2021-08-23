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
# TODO add logic to this function to use it later in the search functionality
def check_phone_number(phone):
    pass
class SearchMan:
    search_error = False

    def __init__(self,model):
        from django.core.paginator import Paginator
        if model == "User":
            from accounts.models import User
            users = User.objects.all().order_by("id")
            self.paginator = Paginator(users, 5)

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

def createExelFile(report_name,headers,**kwargs):
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
    path = os.path.join( desktop_dir, reports_dir)
    # check if it's not created , create it now otherwise ignore
    if os.path.isfile(path):
        os.mkdir(path)
    complete_file_name = os.path.abspath(path)+"/"+report_name+'_'+str(today)+str(current_time)+".xlsx"
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
    file_creation_status = True
    try:
        workBok.close()
        file_creation_status = True
    except:
        file_creation_status = False
    return file_creation_status , complete_file_name


    # return workBok




