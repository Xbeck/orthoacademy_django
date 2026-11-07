from django.urls import path

from courses.views import CourseInvoiceView, CourseListView, CourseDetailView

app_name = "courses"

urlpatterns = [
  path("", CourseListView.as_view(), name='course_list'),
  path("<int:id>/", CourseDetailView.as_view(), name='course_detail'),
  path("<int:pk>/invoice/", CourseInvoiceView.as_view(), name='course_invoice'),
]