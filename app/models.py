from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

STATE_CHOICE=(('Raipur',"CG"),("Kanpur","UP"),('Bhopal',"MP"),("ajmer","Rajsthan"),('Chennai',"TN"),('Hydrabad',"AP"))

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=120)
    locality=models.CharField(max_length=120)
    city=models.CharField(max_length=120)
    state=models.CharField(choices=STATE_CHOICE,max_length=120)
    zipcode=models.IntegerField()
    
    def __str__(self):
        return str(self.id)



CATEGORY_CHOICE=(
    ('M',"Mobile"),
    ('L','Laptop'),
    ('TW',"Top Wear"),
    ('BW',"Bottom Wear"),
)
class ProductDetail(models.Model):
    title=models.CharField(max_length=120)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    descripttion=models.TextField()
    brand=models.CharField(max_length=120)
    category=models.CharField(choices=CATEGORY_CHOICE, max_length=2)
    product_image=models.FileField(upload_to='productimgs',null=True)

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(ProductDetail,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price
        

ORDER_CHOICE=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancle','Cancle'),
)

class ProductPlaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(ProductDetail,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    order_date =models.DateTimeField(auto_now_add=True )
    status=models.CharField(choices=ORDER_CHOICE, max_length=50, default='Pending')
    
    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price