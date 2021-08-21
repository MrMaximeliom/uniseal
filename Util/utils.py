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

def createExelFile(headers,**kwargs):
    import xlsxwriter
    from string import ascii_uppercase
    workBok = xlsxwriter.Workbook("test.xlsx")
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




