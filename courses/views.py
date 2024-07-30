from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from blog.models import Blog
from courses.models import Course, Video, Category, Teacher


class CourseListView(TemplateView):
    template_name = 'courses/course.html'

    def get_context_data(self, **kwargs):
        courses = Course.objects.all()
        categories = Category.objects.all()
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['categories'] = categories
        context['courses'] = courses
        return context


class IndexTemplateView(TemplateView):
    template_name = 'courses/index.html'

    def get_context_data(self, **kwargs):
        courses = Course.objects.all()
        categories = Category.objects.all()
        teachers = Teacher.objects.all()
        blog = Blog.objects.all()
        context = super().get_context_data(**kwargs)
        context['categories'] = categories
        context['courses'] = courses
        context['blog'] = blog
        context['teachers'] = teachers
        return context


class CourseDetailView(TemplateView):
    template_name = 'courses/course-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = Course.objects.get(pk=self.kwargs['pk'])
        videos = Video.objects.filter(course=course)

        context.update({
            'course': course,
            'videos': videos,

        })
        return context


class AboutTemplateView(TemplateView):
    template_name = 'courses/about.html'


class ContactTemplateView(TemplateView):
    template_name = 'courses/contact.html'


class CategoryDetailView(TemplateView):
    template_name = 'courses/category-detail.html'

    def get_context_data(self, **kwargs):
        category = Category.objects.get(pk=self.kwargs['pk'])
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        courses = Course.objects.filter(category=category)
        context.update({'category': category, 'courses': courses})
        return context
