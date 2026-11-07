from django.db import models
from django.contrib.auth.models import AbstractUser

from courses.models import Courses




class CustomUser(AbstractUser):
    phone = models.IntegerField(null=True)
    region = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    profile_picture = models.ImageField(default=f"default_doctor.jpg")
    language = models.CharField(max_length=3, default="uz")
    STAJ_CHOICES = (
            ('student', 'Student'),
            ('ordinat', 'Ordinator'),
            ('magistr', 'Magister'),
            ('doc', 'Doctor')
        )
    staj = models.CharField(max_length=50, choices=STAJ_CHOICES, null=True)

    def __str__(self):
        return f"{self.username}, {self.phone}, {self.region}, {self.province}, {self.city}, {self.profile_picture}, {self.language}"


class Dashboard(models.Model):
    buy_date = models.DateField()
    progres = models.IntegerField(default=0)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class OrthoAcademyData(models.Model):
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED'
        PENDING = "PENDING"
        PAID = "PAID"
        CANCELED = "CANCELED"
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    product_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CANCELED)

    def __str__(self) -> str:
        return self.fullname