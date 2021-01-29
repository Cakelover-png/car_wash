from django.db import models
from management.choices import CAR_TYPES, PAYMENT_TYPES, ORGANIZATION_TYPES
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
        verbose_name = _('Car wash')
        verbose_name_plural = _('Car washes')

    def __str__(self):
        return self.full_name


class Washer(models.Model):
    car_wash = models.ForeignKey(to='management.CarWash', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    personal_id = models.CharField(max_length=11, unique=True)
    payment = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['last_name']
        verbose_name = _('Washer')
        verbose_name_plural = _('Washers')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CarType(models.Model):
    car_wash = models.ForeignKey(to='management.CarWash', on_delete=models.CASCADE)
    type = models.IntegerField(choices=CAR_TYPES)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = _('Car type')
        verbose_name_plural = _('Car types')

    def __str__(self):
        return f"{CAR_TYPES[self.type-1][1]} | {self.car_wash.full_name}"


class Car(models.Model):
    car_type = models.ForeignKey(to='management.CarType', on_delete=models.PROTECT)
    license_plate = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

    def __str__(self):
        return f"{self.license_plate}"


class Order(models.Model):
    washer = models.ForeignKey(to='management.Washer', on_delete=models.PROTECT)
    car = models.ForeignKey(to='management.Car', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    payment_type = models.IntegerField(choices=PAYMENT_TYPES)  # for decoration
    created = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        if self.finish_time:
            return f"{self.finish_time} | {self.car.license_plate}"
        else:
            return f"{'not finished yet'} | {self.car.license_plate}"

    def save(self, *args, **kwargs):
        self.price = self.car.car_type.price
        super(Order, self).save(*args, **kwargs)
