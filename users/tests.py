from django.test import TestCase

from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user


class RegistrationTestCase(TestCase):
  def test_user_account_is_created(self):
    self.client.post(
      reverse("users:register"),
      data={
        "username": "jahon",
        "first_name": "Jahongir",
        "last_name": "Rajabov",
        "email": "test@gmail.com",
        "password": "somepassword"
      }
    )
    
    #  userni olami
    user = CustomUser.objects.get(username="jahon")

    # user malimotlarini test qilamiz
    # self.assertEqual(user.username, "jahon")
    self.assertEqual(user.first_name, "Jahongir")
    self.assertEqual(user.last_name, "Rajabov")
    self.assertEqual(user.email, "test@gmail.com")
    # password ni hash qiymati password ni asil qiymatiga teng emasligini test qilish:
    self.assertNotEqual(user.password, "somepassword")
    # passwordni hash qiymatini test qilamiz:
    self.assertTrue(user.check_password("somepassword"))

  # To'ldirilishi shart bo'lgan qiymatlar, bo'sh yuborilmayotganini test qilish:
  def test_required_fields(self):
    response = self.client.post(
      reverse("users:register"),  # soft code 
      data={
        "first_name": "Jahongir",
        "email": "test@gmail.com",
      }
    )
    user_count = CustomUser.objects.count()

    # bazada user yaratilmaganini test qilish:
    self.assertEqual(user_count, 0)
    # formadagi shart parametrlarni bo'sh kiritganda, beck end dan error qaytishini test qilish:
    self.assertFormError(response, "form", "username", "This field is required.")
    self.assertFormError(response, "form", "password", "This field is required.")

  # email xato kiritlgan holatni test qilish
  def test_invalid_email(self):
    response = self.client.post(
      reverse("users:register"),  # soft code 
      data={
        "username": "jahon",
        "first_name": "Jahongir",
        "last_name": "Rajabov",
        "email": "test-gmail.com",
        "password": "somepassword"
      }
    )
    user_count = CustomUser.objects.count()

    # bazada user yaratilmaganini test qilish:
    self.assertEqual(user_count, 0)
    self.assertFormError(response, "form", "email", "Enter a valid email address.")

  # user unique bo'lishi kerak, ikkita bir xil akkoun bo'lmasligi kerak.
  def test_unique_username(self):
    # user yaratish, bazaga kiritiladi
    self.client.post(
      reverse("users:register"),  # soft code 
      data={
        "username": "jahon",
        "first_name": "Jahongir",
        "last_name": "Rajabov",
        "email": "test@gmail.com",
        "password": "somepassword"
      }
    )
    user_count = CustomUser.objects.count()
    self.assertEqual(user_count, 1)

    # yana bitta birxil username li user yaratishga urinish, xato chiqishi kerak
    response = self.client.post(
      reverse("users:register"),  # soft code 
      data={
        "username": "jahon",
        "first_name": "Jahongir",
        "last_name": "Rajabov",
        "email": "test@gmail.com",
        "password": "somepassword"
      }
    )
    user_count = CustomUser.objects.count()
    self.assertEqual(user_count, 1)
    # formaga backend dan error qaytishini test qilish
    self.assertFormError(response, "form", "username", "A user with that username already exists.")



class LoginTestCase(TestCase):
  # user yaratish uchun metod
  def setUp(self):
    # DRY - Dont repeat yourself
    self.db_user = CustomUser.objects.create(username='bek', first_name="ismli")
    self.db_user.set_password("123")
    self.db_user.save()

  # to'g'ri username va parol kiritilgan holatni test qilamiz
  def test_successful_login(self):
    self.client.post(
      reverse("users:login"),
      data={
        "username": 'bek',
        "password": '123'
      }
    )
    user = get_user(self.client)

    self.assertTrue(user.is_authenticated)

  # noto'g'ri login yo parol kiritilgan holatni test qilish
  def test_wrong_credentials(self):
    # wrong username test
    self.client.post(
      reverse("users:login"),
      data={
        "username": 'wrongusername',
        "password": '123'
      }
    )
    user = get_user(self.client)
    self.assertFalse(user.is_authenticated)

    # wrong password test
    self.client.post(
      reverse("users:login"),
      data={
        "username": 'bek',
        "password": 'wrongpass'
      }
    )
    user = get_user(self.client)
    self.assertFalse(user.is_authenticated)

  # log oput metodini test qilish
  def test_logout(self):
    self.client.login(username="bek", password="123")
    
    self.client.get(reverse("users:logout"))

    user = get_user(self.client)
    self.assertFalse(user.is_authenticated)




# Profil page uchun test
class ProfileTestCase(TestCase):
  # user yaratish uchun metod
  def setUp(self):
    # DRY - Dont repeat yourself
    self.db_user = CustomUser.objects.create(username='utkir', first_name="bekov", last_name="Jahonovich", email="test@utkir.ru")
    self.db_user.set_password("123")
    self.db_user.save()

    # create biznes
    self.b_user = Biznes.objects.create(name='Mini Market', description="Oziq ovqat marketi.", speciality="Market", user_account_id=self.db_user.pk)
    self.b_user.save()

    # create professi
    self.p_user = Profession.objects.create(profession='Doctor', bio="Tramatolog bo'lib 10 yildan beri ishlab kelaman.", user_account_id=self.db_user.pk)
    self.p_user.save()

  # login qilmagan user, login pagega yuborilganini test qilami
  def test_login_required(self):
    response = self.client.get(reverse("users:profile"))

    # 
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

  # profile page detaillari chiqayotganini test qilamiz
  def test_profile_detail(self):
    # userni login qilamiz
    self.client.login(username='utkir', password='123')

    # shu user bilan request yuboramiz
    response= self.client.get(reverse("users:profile"))

    # qaytgan javob saxifada malumotlar borligini tekshiramiz
    #  to'g'ri javobni status kodi 200 ga teng bo'lishi kerak
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.db_user.username)
    self.assertContains(response, self.db_user.first_name)
    self.assertContains(response, self.db_user.last_name)
    self.assertContains(response, self.db_user.email)

 # profile edit page to'g'ri ishlayotganini test qilamiz
  def test_update_profile(self):
    self.client.login(username="utkir", password="123")

    response = self.client.post(
      reverse("users:profile-edit"),
      data={
        "username": self.db_user.username,
        "first_name": self.db_user.first_name,
        "last_name": "Doue",
        "email": "test@bek.com",
      }
    )

    # user dannilarini eski db_user primary_keyi orqali olamiz, taqqoslash uchun
    user = CustomUser.objects.get(pk=self.db_user.pk)

    # db ni refresh qilish va user danilarini qayta olish
    # self.db_user.refresh_from_db()


    self.assertEqual(user.last_name, "Doue")
    self.assertEqual(user.email, "test@bek.com")
    self.assertEqual(response.url, reverse("users:profile"))