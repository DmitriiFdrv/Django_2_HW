from django.http import request
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from basketapp.models import Basket
from mainapp.models import Product
from .models import ProductCategory
from django.shortcuts import get_object_or_404
import random


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return same_products


def index(request):
    context = {
        'title': 'Главная',
        'product': Product.objects.all()[:4]
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)





def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,

        }

        return render(request, 'mainapp/products_list.html', context)


def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', content)