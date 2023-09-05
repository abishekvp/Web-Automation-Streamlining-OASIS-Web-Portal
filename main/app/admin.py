from django.contrib import admin
from .models import User, message
# Register your models here.
admin.site.register(User)
admin.site.register(message)
