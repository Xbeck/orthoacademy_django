from django.contrib import admin

from .models import Courses

@admin.register(Courses)
class CourseAdmin(admin.ModelAdmin):
  list_display = ("title",
                  'image',
                  'short_discription',
                  'discription',
                  'plan',
                  'price',
                  'discount'
                    )
