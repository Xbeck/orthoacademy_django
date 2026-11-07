from typing import Any
from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import PasswordChangeForm

from users.models import CustomUser


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        labels = {
            'username': 'Foydalanuvchi nomi',
            'email': 'Email manzil',
            'password': "Paro'l"
        }
        help_texts = {
            'username': 'Majburiy. 150 yoki undan kam belgi. Faqat harflar, raqamlar va @/./+/-/_.'
        }

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        # send email
        # if user.email:
        #     send_mail(
        #             "Welcom to Ortho Academy",
        #             F"Hi, {user.username}. Welcome to Ortho Academy. Enjoy the watch to course",
        #             "xab60xr@gmail.com",
        #             [user.email]
        #     )


        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', "profile_picture")