from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import redirect
from .models import *


def student_only(function):
    def wrap(request, *args, **kwargs):
        try:
            entry = Student.objects.get(register_num=request.session.get('session_identifier'))
            # print(entry.name)
            return function(request, *args, **kwargs)
        except ObjectDoesNotExist:
            print('not logged')
            return redirect('student_login')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
