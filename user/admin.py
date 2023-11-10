from django.contrib import admin

# Register your models here.
from .models import User, UserConfirmation

admin.site.register(User)
admin.site.register(UserConfirmation)
