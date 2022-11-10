from django.contrib import admin
from .models import Region, DetailRegion

# Register your models here.
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name',]
class DetailRegionAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(Region, RegionAdmin)
admin.site.register(DetailRegion, DetailRegionAdmin)