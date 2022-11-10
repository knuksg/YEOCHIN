from django.contrib import admin
from .models import Hotel

# Register your models here.
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(Hotel, HotelAdmin)