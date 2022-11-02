from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserData)
admin.site.register(UserDataPoint)
admin.site.register(OauthClient)
admin.site.register(ApiKey)
