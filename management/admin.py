from django.contrib import admin
from .models import Location, CarWash, Washer, CarType, Car, Order


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'street_adress')


@admin.register(CarWash)
class CarWashAdmin(admin.ModelAdmin):
    pass


@admin.register(Washer)
class WasherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'personal_id')


@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'finish_time')
    readonly_fields = ('created', 'price')
