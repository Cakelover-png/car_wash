from django.contrib import admin
from .models import Location, CarWash, Employee, Car, Request


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'street_adress')


@admin.register(CarWash)
class CarWashAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'job_position', 'personal_id')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'leather_seats')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('car', 'finish_time')
    readonly_fields = ('created',)
