from django.contrib.postgres.fields import ArrayField
from django.db import models

# categoria cartii
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    section = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# carti
class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = ArrayField(models.CharField(max_length=100))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.title

# vanzari
class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    qty = models.IntegerField(default=0)