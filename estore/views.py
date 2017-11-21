# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *




class ProductViewSet(viewsets.ModelViewSet):
    """
    See all the products listed in the site
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get',]



class ProductRatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be view or edit product rating
    """
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer
    #http_method_names = ['get','post', 'head']
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        order = serializer.validated_data.get('order')
        s_user = order.user
        if self.request.user == s_user:
            serializer.save()
        else:
            raise Exception('Not Same User')


    def partial_update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.order.user != request.user:
            raise Exception('Not Same User')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

class ManufacturerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be view Manufacturer Details
    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    http_method_names = ['get',]

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be add orders
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    def list(self, request):
        queryset = self.queryset.filter(user = request.user)
        return super(OrderViewSet, self).list(request)