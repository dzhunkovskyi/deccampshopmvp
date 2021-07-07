from django.contrib import admin

from shop import models


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name']


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['customer_id']


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
