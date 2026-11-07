from datetime import date
import logging
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
import re
from django.views import View
from django.utils.functional import SimpleLazyObject
# from django.urls import reverse_lazy
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

try:
    from payme.methods.generate_link import GeneratePayLink
except ModuleNotFoundError:
    GeneratePayLink = None
    logging.getLogger(__name__).warning(
        "Payme package is not installed; payment link generation will be unavailable."
    )

from courses.models import Courses
from users.forms import  UserCreateForm, UserUpdateForm
from users.models import CustomUser, Dashboard
from users.models import Order
from config import settings


class RegisterView(View):
  def get(self, request):
    create_form = UserCreateForm()
    context = {
      "form": create_form,
    }
    return render(request, "users/register.html", context=context)

  def post(self, request):
    create_form = UserCreateForm(data=request.POST)

    if create_form.is_valid():
      create_form.save()
      return redirect("users:login")
    else:
      context = {
                "form": create_form,
            }
      return render(request, "users/register.html", context=context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        
        return render(request, "users/login.html", {"login_form": login_form})

    def post(self, request, pk=None):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "Siz muvaffaqiyatli tizimga kirdingiz.")

            whear_from = request.META.get('HTTP_REFERER')
            if re.findall(r"\/\d+\/invoice\/", whear_from):
                pk = pk
                return render(request, 'courses/course_invoice.html', {"course": pk})
            else:
                return redirect("users:dashboard")
        else:
            return render(request, "users/login.html", {"login_form": login_form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id
        return render(request, "users/profile.html", {"user": request.user})


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
            user_update_form = UserUpdateForm(instance=request.user)

            return render(request, "users/edit_profile.html", {"form": user_update_form})

    def post(self, request):
        user_update_form = UserUpdateForm(
        instance=request.user,
        data=request.POST,
        files=request.FILES
        )

        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "Siz profilingizni muvaffaqiyatli yangiladingiz.")

            return redirect("users:profile")

        return render(request, "users:edit_profile.html", {"form": user_update_form})



class PasswordsChangeView(PasswordChangeView):
    def get(self, request):
        password_update_form = PasswordChangeForm(user=request.user)

        return render(request, "users/password_change_form.html", {"form": password_update_form})
    
    def post(self, request):
        password_update_form = PasswordChangeForm(
                    user=request.user,
                    data=request.POST,
                    files=request.FILES
        )

        if password_update_form.is_valid():
            password_update_form.save()
            message = messages.success(request, "Parolingizni muvaffaqiyatli yangiladingiz! Saytga yangi parol bilan kirishingiz mumkin.")

            login_form = AuthenticationForm()
            return render(request, "users/login.html", {"message": message, "login_form": login_form})
        return render(request, "users/password_change_form.html", {"form": password_update_form})


class LogoutView(LoginRequiredMixin, View):
  def get(self, request):
    logout(request)
    messages.info(request, "You have successfully logged out.")

    return redirect("landing_page")


class UserDashboardView(LoginRequiredMixin, View):
    def get(self, request, id=None):
        dashboards = Dashboard.objects.filter(user=request.user)

        user_courses = [(i, dashboard.course) for i, dashboard in enumerate(dashboards)]
        progres = {}
        for dashboard in dashboards:
            course_id = dashboard.course.id
            progres_value = dashboard.progres
            course = Courses.objects.get(id=course_id)
            progres[course.id] = int( ( 100 / course.count_videos ) * progres_value )


            logging.info(user_courses)
            logging.info(dashboards)
            logging.info(progres)

        context = {
            'user_courses': user_courses,
            'progres': progres,
        }
        return render(request, 'users/dashboard.html', context)


class CourseProgresView(LoginRequiredMixin, View):
    def get(self, request, id, num=1):
        course = get_object_or_404(Courses, id=id)

        user = request.user
        if isinstance(user, SimpleLazyObject):
            user = user._wrapped
        
        dashboard = Dashboard.objects.get(user_id=user.id, course_id=id)
        if num == 1:
            progres = int((100 / course.count_videos) * 0)
        else:
            progres = int((100 / course.count_videos) * (num - 1))

        words = [
                "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty",
                "Twenty_One", "Twenty_Two", "Twenty_Three", "Twenty_Four", "Twenty_Five", "Twenty_Six", "Twenty_Seven", "Twenty_Eight", "Twenty_Nine", "Thirty",
                "Thirty_One", "Thirty_Two", "Thirty_Three", "Thirty_Four", "Thirty_Five", "Thirty_Six", "Thirty_Seven", "Thirty_Eight", "Thirty_Nine", "Forty",
                "Forty_One", "Forty_Two", "Forty_Three", "Forty_Four", "Forty_Five", "Forty_Six", "Forty_Seven", "Forty_Eight", "Forty_Nine", "Fifty"
            ]

        video_range = range(1, course.count_videos + 1)

        try:
            dashboard.progres = num - 1
            dashboard.save()

            logging.info(f"Данные успешно сохранены: {dashboard}")
        except Exception as e:
            logging.error(f"Ошибка сохранения данных: {e}")

        context = {
            'course': course,
            'blocktitles': {i: word for i, word in enumerate(words[ : 3])},
            'blockitems': video_range,
            'len': len(video_range),
            'progres': progres,
            'id': num
        }

        return render(request, 'users/course_progres.html', context)