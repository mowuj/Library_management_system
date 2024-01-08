from django.db import models
from django.contrib.auth.models import User
from .constants import RATING
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug =models.SlugField(max_length=100,unique=True,blank=True,null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField()
    image = models.ImageField(
        upload_to='media/uploads/', null=True, blank=True)
    category = models.ManyToManyField(Category, related_name="books")
    borrowing_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.title

class Review(models.Model):
    user=models.ForeignKey(User,related_name="reviews", on_delete=models.CASCADE)
    book=models.ForeignKey(Book,related_name='reviews',on_delete=models.CASCADE)
    body=models.TextField()
    rating=models.IntegerField(choices=RATING)
    models.DateTimeField( auto_now_add=True)
    timestamps=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username