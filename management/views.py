from django.shortcuts import render
from django.db.models import Sum, Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime
from .models import CarWash


def homepage(request):
    return render(request, 'management/homepage.html')


def car_washes(request):
    car_washes = CarWash.objects.all()
    return render(request, 'management/car_washes.html',
                  context={'car_washes': car_washes}
                  )


def car_wash_detail(request, cw_pk):
    car_wash = get_object_or_404(CarWash, pk=cw_pk)
    washed_cars = car_wash.washer_set.annotate(
        orders_count=Count('order', filter=Q(order__finish_time__isnull=False)),
    ).aggregate(Sum('orders_count'))['orders_count__sum']
    washed_cars = washed_cars if washed_cars else 0
    return render(request, 'management/car_wash_detail.html',
                  context={'car_wash': car_wash,
                           'washed_cars': washed_cars}
                  )


def washers(request, cw_pk):
    car_wash = get_object_or_404(CarWash, pk=cw_pk)
    washers = car_wash.washer_set.all()
    washers_dict = {}

    for washer in washers:
        all_finished = washer.order_set.filter(
            finish_time__isnull=False)
        yearly_finished = all_finished.filter(
            finish_time__gt=timezone.now()-datetime.timedelta(days=365))
        monthly_finished = yearly_finished.filter(
            finish_time__gt=timezone.now()-datetime.timedelta(days=30))
        weakly_finished = monthly_finished.filter(
            finish_time__gt=timezone.now()-datetime.timedelta(days=7))
        weakly_pay = weakly_finished.aggregate(Sum('price'))['price__sum']
        monthly_pay = monthly_finished.aggregate(Sum('price'))['price__sum']
        yearly_pay = yearly_finished.aggregate(Sum('price'))['price__sum']
        washers_dict[washer.id] = {
            'weakly_washed': weakly_finished.count(),
            'weakly_pay': round(weakly_pay/2, 2) if weakly_pay else 0.0,
            'monthly_washed': monthly_finished.count(),
            'monthly_pay': round(monthly_pay/2, 2) if monthly_pay else 0.0,
            'yearly_washed': yearly_finished.count(),
            'yearly_pay': round(yearly_pay/2, 2) if yearly_pay else 0.0,
            'all_washed': all_finished.count(),
        }

    return render(request, 'management/washers.html',
                  context={'washers': washers,
                           'washers_dict': washers_dict}
                  )
