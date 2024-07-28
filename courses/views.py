from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from courses.models import Course


class IndexTemplateView(TemplateView):
    template_name = 'index/index.html'


class CourseTemplateView(TemplateView):
    template_name = 'courses/course.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context
