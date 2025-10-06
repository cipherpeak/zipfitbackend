from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee,ProductionApproval



admin.site.register(Employee)
admin.site.register(ProductionApproval)