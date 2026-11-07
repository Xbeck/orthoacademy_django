from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config.views import LandingView


urlpatterns = [
    path('', LandingView.as_view(), name='landing_page'),
    path('users/', include("users.urls")),
    path('users/', include("django.contrib.auth.urls")),
    path('courses/', include("courses.urls")),
    # path("payments/merchant/", PaymeCallBackAPIView.as_view()),
    # path("payments/create-order/", CreateOrderView.as_view()),


    path('admin/', admin.site.urls),
    # path('admin/', AdminPanelLoginView.as_view(), name='admin_login'),
]


# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)