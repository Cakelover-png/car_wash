from django.urls import path
from .views import homepage, car_washes, car_wash_detail, washers


urlpatterns = [
    path('', homepage, name='homepage'),
    path('car_washes/', car_washes, name='car_washes'),
    path('car_washes/<int:cw_pk>/details', car_wash_detail, name='cw_detail'),
    path('car_washes/<int:cw_pk>/washers', washers, name='washers'),
]
