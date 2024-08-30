from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User





class UserProfile(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_profiles',  # Custom related name to avoid clashes
        related_query_name='user_profile',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_profiles',  # Custom related name to avoid clashes
        related_query_name='user_profile',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='productimages/')
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    reorderlevel = models.IntegerField(default=0)
    category = models.CharField(max_length=100, default='Uncategorized')
    is_ordered = models.BooleanField(default=False)
    
    def is_at_reorder_level(self):
        return self.quantity <= self.reorderlevel  # Modified condition to include equal to

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure quantity, price, and reorder level do not go below zero
        if self.quantity < 0:
            self.quantity = 0
        if self.price < 0:
            self.price = 0
        if self.reorderlevel < 0:
            self.reorderlevel = 0
        super().save(*args, **kwargs)
        
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def create_category(cls, name):
        category, created = cls.objects.get_or_create(name=name)
        return category

    @classmethod
    def delete_category(cls, name):
        try:
            category = cls.objects.get(name=name)
            category.delete()
            return True
        except cls.DoesNotExist:
            return False
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart for {self.user.username}: {self.product.name}"
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.fullname} placed on {self.created_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"
    



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)
    is_from_delivered_order = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'





class Supplier(models.Model):
    company_name = models.CharField(max_length=100,default='Not provided')
    username = models.CharField(max_length=50, unique=True,null=True)
    password = models.CharField(max_length=50,null=True)
    email = models.EmailField(unique=True)
    address = models.TextField(default="No address provided")
    
    

    def __str__(self):
        return self.company_name

class PurchaseOrderItem(models.Model):
    # Your fields and configurations here
    pass



    
class PurchaseOrderstatus(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

def get_default_status():
    # Retrieve or create the 'pending' status object
    default_status, created = PurchaseOrderstatus.objects.get_or_create(status='pending')
    return default_status

class PurchaseOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(PurchaseOrderstatus, on_delete=models.CASCADE, default=get_default_status)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - Quantity: {self.quantity} - Date: {self.order_date}"

