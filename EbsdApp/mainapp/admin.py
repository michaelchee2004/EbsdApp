from django.contrib import admin
from .models import *

models_list = [Option,
               Year,
               Capital,
               Opex,
               Capacity,
               Demand]

admin.site.register(models_list)