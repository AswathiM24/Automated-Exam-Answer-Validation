from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Student)
admin.site.register(Login)
admin.site.register(Answers)