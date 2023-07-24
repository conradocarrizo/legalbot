from django.contrib import admin
from societies.models import Rut, Society, Person

# Register your models here.
admin.site.register((Rut, Society, Person))
