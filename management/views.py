from django.shortcuts import render
from decimal import Decimal
from django.db.models import Sum, Count, Q, F, ExpressionWrapper, DecimalField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import CarWash, Order, Car
from .forms import CarForm, OrderForm


def homepage(request):
    return render(request, 'management/homepage.html')


def car_washes(request):
    car_washes = CarWash.objects.all()
    return render(request, 'management/car_washes.html',
                  context={'car_washes': car_washes}
                  )


def car_wash_detail(request, cw_pk):
    car_wash = get_object_or_404(CarWash, pk=cw_pk)
    # washed_cars = car_wash.washer_set.annotate(
    #     orders_count=Count('order', filter=Q(order__finish_time__isnull=False)),
    # ).aggregate(Sum('orders_count'))['orders_count__sum']
    washed_cars = Order.objects.filter(finish_time__isnull=False,
                                       washer__car_wash_id=car_wash.id).count()
    washed_cars = washed_cars if washed_cars else 0
    return render(request, 'management/car_wash_detail.html',
                  context={'car_wash': car_wash,
                           'washed_cars': washed_cars}
                  )


def washers(request, cw_pk):
    car_wash = get_object_or_404(CarWash, pk=cw_pk)

    washers = car_wash.washer_set.annotate(
        washer_earned_money=ExpressionWrapper(
            F('order__price')/Decimal('2.00'), output_field=DecimalField())
    ).annotate(
        all_washed=Count('order', filter=Q(order__finish_time__isnull=False)),

        all_pay=Sum('washer_earned_money', filter=Q(order__finish_time__isnull=False)),

        yearly_washed=Count('order', filter=Q(
            order__finish_time__gte=timezone.now() - timezone.timedelta(days=356))),

        yearly_pay=Sum('washer_earned_money', filter=Q(
            order__finish_time__gte=timezone.now() - timezone.timedelta(days=365))),

        monthly_washed=Count('order', filter=Q(
            order__finish_time__gte=timezone.now() - timezone.timedelta(days=30))),

        monthly_pay=Sum('washer_earned_money', filter=Q(
            order__finish_time__gte=timezone.now() - timezone.timedelta(days=30))),

        weekly_washed=Count('order', filter=Q(
            order__finish_time__gte=timezone.now() - timezone.timedelta(days=7))),

        weekly_pay=Sum('washer_earned_money', filter=Q(
            order__finish_time__gte=timezone.now() - timezone.timedelta(days=7))),
    )

    return render(request, 'management/washers.html',
                  context={'washers': washers, }
                  )


def cars(request, cw_pk):
    car_wash = get_object_or_404(CarWash, pk=cw_pk)
    page = request.GET.get('page', 1)
    car_list = Car.objects.filter(car_type__car_wash_id=car_wash.id)
    paginator = Paginator(car_list, 4)
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)
    car_form = CarForm(car_wash.id)
    if request.method == 'POST':
        car_form = CarForm(car_wash.id, data=request.POST)
        if car_form.is_valid():
            car_form.save()
            return render(request, 'management/cars.html',
                          context={'cars': cars,
                                   'form': car_form,
                                   'is_succ': True,
                                   })
    return render(request, 'management/cars.html',
                  context={'cars': cars,
                           'form': car_form
                           })


def order(request, cw_pk):
    car_wash = get_object_or_404(CarWash, pk=cw_pk)
    order_form = OrderForm(car_wash.id)
    if request.method == 'POST':
        order_form = OrderForm(car_wash.id, data=request.POST)
        if order_form.is_valid():
            order_form.save()
            return render(request, 'management/order.html',
                          context={'car_wash': car_wash,
                                   'form': order_form,
                                   'is_succ': True})
    return render(request, 'management/order.html',
                  context={'car_wash': car_wash,
                           'form': order_form})
