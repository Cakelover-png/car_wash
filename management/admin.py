from django.contrib import admin
from .models import Location, CarWash, Employee, Car, Request


admin.site.register(Location)
admin.site.register(CarWash)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'job_position')


admin.site.register(Employee, EmployeeAdmin)


class CarAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'leather_seats')


admin.site.register(Car, CarAdmin)


class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Request, RequestAdmin)
