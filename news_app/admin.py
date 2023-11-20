from django.contrib import admin
from .models import News, History, SavedNews, Comment

admin.site.register(History)
admin.site.register(SavedNews)
admin.site.register(Comment)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_filter = ("category", )