import datetime
import logging
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.paginator import Paginator

from courses.models import Courses
from users.models import CustomUser, Dashboard, OrthoAcademyData



class CourseListView(View):
    def get(self, request):
        course_objs = Courses.objects.all().order_by('id')

        page_size = request.GET.get("page_size", 10)
        paginator = Paginator(course_objs, page_size)

        page_num = request.GET.get("page", 1) # default 1 - page chiqadi
        page_object = paginator.get_page(page_num)

        ortho_academy = OrthoAcademyData.objects.get(id=1)

        context = {
                    "page_obj": page_object,
                    "user": request.user,
                    "courses": course_objs,
                    "ortho_academy": ortho_academy
                    }
        return render(request, "courses/course_list.html", context)


class CourseDetailView(View):
    def get(self, request, id):
        course = Courses.objects.get(id=id)
        user = request.user

        try:
            dashboard = Dashboard.objects.get(user_id=user.id, course_id=id)
        except Dashboard.DoesNotExist:
            dashboard = None

        print(dashboard)
        logging.info(dashboard)

        if dashboard == None:
            if course.price == 0:

                dashboard_entry = Dashboard(
                    buy_date=datetime.date.today(),
                    progres=0,
                    course=course,
                    user=user)
                dashboard_entry.save()
            else:
                pass
        return render(request, "courses/course_detail.html", {"user": user, "course": course})



class CourseInvoiceView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # LoginRequiredMixin - shu klass o'zi userni login qilganini tekshirib beradi
        # course_obj = Courses.objects.get(id=id)

        # add course to DB
        # buy_time = datetime.datetime.now()
        # user_id = request.user.id
        # course_id = pk

        # new_obj = Dashboard(buy_data=buy_time, progres=0, course=course_id, user=user_id)
        # new_obj.save()

        amount = 100000
        order_id = '123456789'

        # paycom = Paycom()

        # url = paycom.create_initialization(amount=amount,
        #                                    order_id=order_id,
        #                                    return_url='https://orthoacademy.com/payment/success/')
        # print(url)

        # return render(request, url, {"user": request.user})
    
    # def get(self, request, pk):
    #     course = get_object_or_404(Courses, pk=pk)
    #     # Your logic here
    #     return HttpResponse(f"Invoice for course: {course.name}")