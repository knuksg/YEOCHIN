from django.contrib import admin
from .models import Friend, Friend_Comment, FriendRequest

# Register your models here.

# Register your models here.
class FriendAdmin(admin.ModelAdmin):
    list_display = ['title',]

class Friend_CommentAdmin(admin.ModelAdmin):
    list_display = ['content',]
    
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['friend',]

admin.site.register(Friend, FriendAdmin)
admin.site.register(Friend_Comment, Friend_CommentAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)