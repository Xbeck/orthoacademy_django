import re
from django.shortcuts import redirect, render
from django.views import View

from courses.models import Courses
from users.models import Dashboard, OrthoAcademyData



# Courses obj ni landing page ga uzatamiz
class LandingView(View):
    def get(self, request, course_id=None):
        courses = Courses.objects.all().order_by('id')
        ortho_academy = OrthoAcademyData.objects.get(id=1)

        context = {
                    "user": request.user,
                    "courses": courses,
                    "ortho_academy": ortho_academy
                    }

        return render(request, "landing.html", context)