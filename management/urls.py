from django.urls import path
from .views import homepage, car_washes, car_wash_detail, washers, order, cars, car_json


urlpatterns = [
    path('', homepage, name='homepage'),
    path('car_washes/', car_washes, name='car_washes'),
    path('car_washes/<int:cw_pk>/details', car_wash_detail, name='cw_detail'),
    path('car_washes/<int:cw_pk>/washers', washers, name='washers'),
    path('car_washes/<int:cw_pk>/cars', cars, name='cars'),
    path('order/<int:cw_pk>', order, name='order'),
    path('car_json/<int:cw_pk>', car_json, name='car_json')
]
