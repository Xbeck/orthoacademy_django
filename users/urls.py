from django.urls import path
from django.views.generic.base import TemplateView


from .views import CourseProgresView, PasswordsChangeView, RegisterView, LoginView, ProfileView, LogoutView, ProfileUpdateView, UserDashboardView


app_name = "users"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile_edit/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('course_progres/<int:id>/', CourseProgresView.as_view(), name='course_progres'),
    path('course_progres/<int:id>/<int:num>', CourseProgresView.as_view(), name='course_progres'),
    
    path('password_change/', PasswordsChangeView.as_view(), name='password_change_form'),
    path('password_change/done/', TemplateView.as_view(template_name='password_change_done.html'), name='password_change_done'),
]