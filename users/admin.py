from django.contrib import admin

from .models import CustomUser, Order, OrthoAcademyData



@admin.register(CustomUser)
class UsersAdmin(admin.ModelAdmin):
  list_display = ("username", 'last_name', 'first_name',)


@admin.register(OrthoAcademyData)
class OrthoAcademy(admin.ModelAdmin):
  list_display = ("address", 'phone',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ("fullname", 'email', 'product_name', 'amount', 'status')