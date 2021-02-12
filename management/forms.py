from django.forms import ModelForm
from management.choices import PAYMENT_TYPES
from .models import Car, CarType, Order, Washer
from django.forms import ModelChoiceField, TypedChoiceField, CharField
from django.core.validators import MinLengthValidator


class CarForm(ModelForm):
    car_type = ModelChoiceField(empty_label='Choose the car type', queryset=None)
    license_plate = CharField(validators=[MinLengthValidator(6)])

    class Meta:
        model = Car
        fields = '__all__'

    def __init__(self, cw_pk=None, **kwargs):
        super(CarForm, self).__init__(**kwargs)
        self.fields['car_type'].queryset = CarType.objects.filter(car_wash_id=cw_pk)


class OrderForm(ModelForm):
    car = ModelChoiceField(empty_label='Choose the car', queryset=None)
    washer = ModelChoiceField(empty_label='Choose the washer', queryset=None)
    payment_type = TypedChoiceField(choices=PAYMENT_TYPES)

    class Meta:
        model = Order
        fields = ('washer', 'car', 'washer', 'payment_type')

    def __init__(self, cw_pk=None, **kwargs):
        super(OrderForm, self).__init__(**kwargs)
        self.fields['car'].queryset = Car.objects.filter(car_type__car_wash_id=cw_pk)
        self.fields['washer'].queryset = Washer.objects.filter(car_wash_id=cw_pk)
