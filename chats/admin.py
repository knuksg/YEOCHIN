from django.contrib import admin
from .models import Room, Message

# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name',]

class MessageAdmin(admin.ModelAdmin):
    list_display = ['content',]

admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)