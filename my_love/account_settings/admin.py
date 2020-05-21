from django.contrib import admin

from .models import *


# class ChoiceAdmin(admin.StackedAdmin):

class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'surname', 'country')
    search_fields = ['name', 'surname']

    def username(self, instance):
        return instance.user.username

    username.short_description = 'User'


class AboutYouAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ['name', 'surname']

    def username(self, instance):
        return instance.user.username

    username.short_description = 'User'


admin.site.register(MusicType)
admin.site.register(Genres)
admin.site.register(Films)
admin.site.register(Books)
admin.site.register(Hobbies)
admin.site.register(Foods)
admin.site.register(Countries)
admin.site.register(Gallery)

admin.site.register(AboutMe, AboutMeAdmin)
admin.site.register(AboutYou, AboutYouAdmin)