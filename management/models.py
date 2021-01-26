from django.db import models
from management.choices import JOBS, PAYMENT_TYPES, ORGANIZATION_TYPES
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    city = models.CharField(max_length=100)
    street_adress = models.CharField(max_length=100, unique=True)
    zip_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return f"{self.city} | {self.street_adress}"


class CarWash(models.Model):
    full_name = models.CharField(max_length=50, unique=True)
    location = models.OneToOneField(to='management.Location',
                                    on_delete=models.PROTECT)
    organzation_type = models.IntegerField(choices=ORGANIZATION_TYPES)
    tax_id = models.CharField(max_length=10, unique=True)
    creation_time = models.DateTimeField()

    class Meta:
        verbose_name = _('CarWash')
        verbose_name_plural = _('CarWashes')

    def __str__(self):
        return self.full_name


class Employee(models.Model):
    car_wash = models.ForeignKey(to='management.CarWash', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    personal_id = models.CharField(max_length=11, unique=True)
    job_position = models.IntegerField(choices=JOBS)
    salary = models.PositiveIntegerField()

    class Meta:
        ordering = ['last_name']
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    car_brand = models.CharField(max_length=50, blank=True, null=True)
    car_size = models.FloatField(blank=True, null=True)  # in m^3
    leather_seats = models.BooleanField(default=False)
    license_plate = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

    def __str__(self):
        return f"{self.license_plate}"


class Request(models.Model):
    employee = models.ForeignKey(to='management.employee', on_delete=models.PROTECT)
    car = models.ForeignKey(to='management.Car', on_delete=models.CASCADE)
    payment_type = models.IntegerField(choices=PAYMENT_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')

    def __str__(self):
        if self.finish_time:
            return f"{self.finish_time} | {self.car.license_plate}"
        else:
            return f"{'not finished yet'} | {self.car.license_plate}"
