from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def my_paginator(page, obj_list, per_page):
    paginator = Paginator(obj_list, per_page)
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    return objs
