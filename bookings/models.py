from django.db import models

# Create your models here.
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = ('pending', 'Pending')
        CONFIRMED = ('confirmed', 'Confirmed')
        CANCELLED = ('cancelled', 'Cancelled')
        DELIVERED=("delivered","Delivered") 
    photographer=models.EmailField()
    client=models.EmailField()
    price=models.PositiveIntegerField()
    date_of_booking=models.DateField()
    Accessories=models.CharField(max_length=100)
    cameras=models.PositiveIntegerField()
    staff=models.PositiveIntegerField()
    phone=models.CharField(max_length=10)
    package=models.ForeignKey("packages.Package",on_delete=models.SET_NULL,null=True,blank=True)
    drone=models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client', 'package'], name='unique_client_package')
        ]
    
