from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import redirect
from .models import *


def teacher_only(function):
    def wrap(request, *args, **kwargs):
        try:
            entry = Teacher.objects.get(admin_code=request.session.get('tech_session'))
            return function(request, *args, **kwargs)
        except ObjectDoesNotExist:
            print('not logged')
            return redirect('teacher_login')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
