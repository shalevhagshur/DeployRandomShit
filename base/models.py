from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    image = models.ImageField(null=True,blank=True,default='/placeholder.png')
    
    def __str__(self):
           return self.description




class Product(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True, upload_to='product', default='placeholder.png')  # Define the 'upload_to' attribute
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.description

    @property
    def image_url(self):
        if self.image:
            # Change 'your_server_url' to your actual server URL
            return f'http://127.0.0.1:8000{self.image.url}'
        else:
            return ''
        
class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    orderdate = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time when created
    image = models.CharField(max_length=200, null=True, blank=True, default='/placeholder.png')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order for {self.amount} {self.product.description}"