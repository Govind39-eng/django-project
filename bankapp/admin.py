from django.contrib import admin
from . models import Account, AdminLogin, Statement
# Register your models here.
admin.site.register(Account)
admin.site.register(AdminLogin)
admin.site.register(Statement)