from django.contrib import admin
from .models import Location, CarWash, Employee, Car, Request


admin.site.register(Location)
admin.site.register(CarWash)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'job_position')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'leather_seats')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
