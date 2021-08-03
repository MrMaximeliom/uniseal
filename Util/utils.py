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