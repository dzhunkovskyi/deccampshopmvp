import uuid

from django.db import models
from django.db.models import Q
from django.utils import timezone


class Customer(models.Model):
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    chat_id = models.IntegerField('Chat ID', default=0)

    first_name = models.CharField('First Name', default='', max_length=100)
    last_name = models.CharField('Lats Name', default='', max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + '---' + 'chat_id: ' + self.chat_id


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    title = models.CharField('Title', default='', max_length=100)
    price = models.FloatField('Price', default=0.0)

    def __str__(self):
        return self.title + ' ' + self.price



class Order(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    customer_id = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.deletion.CASCADE)

    products = models.ManyToManyField(Product)
    total_price = models.FloatField('Total price', default=0.0)

    def __str__(self):
        return self.customer_id + ' --- ' + self.request_data
