from django.db import models
from author.models import AuthorProfile
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='products_category')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='products')
    price = models.IntegerField()
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)
    is_stock_avaialable = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)
    # inventory = models.IntegerField(default=1)

    def __str__(self):
        return self.name

ORDER_STATUS_CHOICES = [
        ('PLACED', 'PLACED'),
        ('SHIPPED', 'SHIPPED'),
        ('OUT_FOR_DELIVERY', 'OUT FOR DELIVERY'),
        ('DELIVERED', 'DELIVERED')
    ]
class Order(models.Model):
    status = models.CharField(max_length=100,choices=ORDER_STATUS_CHOICES,default='PLACED')
    amount = models.IntegerField()
    details = models.TextField()
    delivery_address = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # is_draft = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    # inventory = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id) + self.user.username
    

