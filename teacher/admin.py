from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Teacher)
admin.site.register(Paper)
admin.site.register(Questions)