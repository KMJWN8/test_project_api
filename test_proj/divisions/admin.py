from django.contrib import admin

from .models import Department, Division, Employee, Service, Team

# Register your models here.

admin.site.register(Service)
admin.site.register(Department)
admin.site.register(Division)
admin.site.register(Team)
admin.site.register(Employee)
