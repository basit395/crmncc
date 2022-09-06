from django.contrib import admin

from .models import Profile,thejobtitle




class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','jobtitle','jobtitle_detail','region',)
    ordering = ('user',)
    search_fields = ('user',)

admin.site.register(Profile, ProfileAdmin)

class thejobtitleAdmin(admin.ModelAdmin):
    list_display = ('jobtitle_name',)
    ordering = ('jobtitle_name',)
    search_fields = ('jobtitle_name',)

admin.site.register(thejobtitle, thejobtitleAdmin)
