from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    days = models.IntegerField()
    description = models.TextField()
    image_url = models.CharField(max_length=500, default="https://via.placeholder.com/300")
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    booking_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Confirmed')

    def __str__(self):
        return f"{self.user.username} - {self.package.name}"
    
    # CONTACT MODEL (User queries ke liye)
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"