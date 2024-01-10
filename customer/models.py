from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER
# Create your models here


class CustomerModel(models.Model):
    user=models.OneToOneField(User, related_name="customer",on_delete=models.CASCADE)
    gender=models.CharField(max_length=10,choices=GENDER)
    customer_id=models.IntegerField(unique=True)
    phone=models.CharField(max_length=12)
    balance=models.DecimalField(decimal_places=2,max_digits=12,default=0)
    street_address=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    country=models.CharField(max_length=50)

    def __str__(self):
        return self.user.username