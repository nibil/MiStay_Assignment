# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models import Avg

# Create your models here.


class Product(models.Model):
	name = models.CharField(max_length=32)
	product_code = models.CharField(max_length=10)
	product_type= models.CharField(max_length=10)
	slug = models.SlugField(max_length=150)
	description = models.TextField(null = True, blank = True)
	manufacturer = models.ForeignKey('Manufacturer')
	photo = models.ImageField(upload_to='product_photo',blank=True)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	quantity = models.IntegerField()
	availability = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		if self.quantity == 0:
			self.availability = False
		if self.product_code =="":
			self.product_code = self.name.capitalize().replace(" ", "")
		if self.slug == "":
			self.slug = "http://127.0.0.1:8000/"+self.product_type.replace(" ", "")+self.name.replace(" ", "")+"/"+self.product_code
		super(Product, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	@property
	def product_rating(self):
		productrating = ProductRating.objects.filter(product = self).aggregate(Avg('rating'))
		rating = productrating.get('rating__avg')
		return rating


class Manufacturer(models.Model):
	name = models.CharField(max_length=32)
	manufacturer_code = models.CharField(max_length=10)
	address = models.TextField()

	def __str__(self):
		return self.name

class Order(models.Model):
	product = models.ForeignKey(Product)
	user = models.ForeignKey(User)
	quantity = models.PositiveIntegerField()
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Order Initated Date')
	
class ProductRating(models.Model):
	order = models.ForeignKey(Order)
	product = models.ForeignKey(Product)
	rating = models.PositiveIntegerField(validators=[MaxValueValidator(5),])
	timestamp = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if self.product == None:
			self.product = self.order.product
		super(ProductRating, self).save(*args, **kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)