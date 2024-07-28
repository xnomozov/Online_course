from django.shortcuts import render
from django.views.generic import ListView, TemplateView

# Create your views here.
from teachers.models import Teacher


class TeacherListView(TemplateView):
    template_name = 'teachers/teacher.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.all()
        return context
