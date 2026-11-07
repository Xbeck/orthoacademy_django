from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.core.mail import send_mail

from users.models import CustomUser
from users.tasks import send_email


@receiver(signal=post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    print("Created", created)
    print("SIGNAL HANDLER CALLED")

    if created:
        send_email.delay(
                "Welcom to Ortho Academy",
                F"Hi, {instance.username}. Welcome to Ortho Academy. Enjoy the watch to course",
                [instance.email]
        )
        # send_mail(
        #         "Welcom to Ortho Academy",
        #         F"Hi, {instance.username}. Welcome to Ortho Academy. Enjoy the watch to course",
        #         "xab60xr@gmail.com",
        #         [instance.email]
        # )