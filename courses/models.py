from django.db import models


class Courses(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(default="default_course_img.jpg")
    short_discription = models.TextField(null=True, blank=True)
    discription = models.TextField(null=True, blank=True)
    plan = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    count_videos = models.IntegerField(default=0)
    time_video = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}, {self.short_discription}, {self.discription}, {self.plan}, {self.price}, {self.discount}, {self.image}"