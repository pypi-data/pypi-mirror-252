from django.contrib import admin
from .models import JWTToken

class JWTTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')

admin.site.register(JWTToken, JWTTokenAdmin)