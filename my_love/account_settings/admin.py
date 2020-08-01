from django.contrib import admin

from .models import *


# class ChoiceAdmin(admin.StackedAdmin):

class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('username', 'country')

    def username(self, instance):
        return instance.user.username

    username.short_description = 'User'


class AboutYouAdmin(admin.ModelAdmin):
    list_display = ('username',)

    def username(self, instance):
        return instance.user.username

    username.short_description = 'User'


admin.site.register(AboutMe, AboutMeAdmin)
admin.site.register(AboutYou, AboutYouAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Questionary)
