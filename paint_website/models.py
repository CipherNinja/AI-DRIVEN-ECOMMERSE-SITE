from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from hashids import Hashids
# Create your models here.

class Our_Product(models.Model):
    product_image = models.ImageField(upload_to='product')
    product_name = models.CharField(max_length=500)
    product_detail = models.CharField(max_length=300)
    product_price = models.CharField(max_length=80)

    def __str__(self):
        return f"""
        {self.product_name} {self.product_detail} {self.product_price}
"""

class Top_Product(models.Model):
    product_image = models.ImageField(upload_to="top")
    product_name = models.CharField(max_length=500)
    product_detail = models.CharField(max_length=300)
    product_price = models.CharField(max_length=80)

    def __str__(self):
        return f"""
        {self.product_image} {self.product_name} {self.product_detail} {self.product_price}
"""

class Blog_Event(models.Model):
    blog_image = models.ImageField(upload_to="blog")
    blog_name = models.CharField(max_length=500)
    blog_detail = models.CharField(max_length=300)
    blog_date = models.DateField(default='')

    def __str__(self):
        return f"""
        {self.blog_image} {self.blog_name} {self.blog_detail} {self.blog_date}
"""


class UserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user} {self.address} {self.phone_number}"

hashids = Hashids(salt="your_default_salt_here", min_length=10) 
class AllOrderDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Our_Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    delivery_status = models.BooleanField(default=False)
    delivery_id = models.CharField(max_length=50,default=hashids.encode(0))
    delivery_date = models.DateTimeField(default=datetime.now)
    order_date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
            # Generate and save encrypted ID before saving the object
            if not self.delivery_id:
                self.delivery_id = hashids.encode(self.pk)
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Order for {self.user.username} --> {self.product.product_name}\n Quantity: {self.quantity}\n Price: {float(self.product.product_price) * float(self.quantity)}\nDelivery status{self.delivery_status}\n Order Date: {self.order_date}"

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Our_Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product.product_name} (Quantity: {self.quantity})"