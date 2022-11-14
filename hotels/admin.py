from django.contrib import admin
from .models import Hotel, HotelReview

# Register your models here.
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name',]

class HotelReviewAdmin(admin.ModelAdmin):
    list_display = ['title',]

admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelReview, HotelReviewAdmin)