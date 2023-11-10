from django.contrib import admin
from .models import News, History, SavedNews, Comment

admin.site.register(News)
admin.site.register(History)
admin.site.register(SavedNews)
admin.site.register(Comment)