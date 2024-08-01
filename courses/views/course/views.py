from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from blog.models import Blog
from courses.forms import CourseCommentForm, StudentForm
from courses.models import Course, Video, Category, Teacher, CourseComment


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
        blogs = Blog.objects.all()
        comments = CourseComment.objects.all().order_by('-created_at')[:3]
        form = StudentForm()

        context = super().get_context_data(**kwargs)
        context['categories'] = categories
        context['courses'] = courses
        context['blogs'] = blogs
        context['teachers'] = teachers
        context['form'] = form
        context['comments'] = comments
        return context

    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.email = request.user.email
            student.name = request.user.username
            student.user = request.user
            student.password = request.user.password
            request.user.is_student = True
            student.save()
            messages.success(request, 'Thank you! You are welcome to study!')
            return redirect('courses')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class CourseDetailView(TemplateView):
    template_name = 'courses/course-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CourseCommentForm()
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        videos = Video.objects.filter(course=course)
        comments = CourseComment.objects.filter(course_id=course)[:3]
        context.update({
            'course': course,
            'videos': videos,
            'form': form,
            'comments': comments

        })
        return context

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        form = CourseCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.student = request.user
            comment.name = request.user.username
            comment.email = request.user.email
            comment.course_id = course
            comment.is_published = True
            comment.save()
            return redirect('course_detail', pk=course.pk)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class AboutTemplateView(TemplateView):
    template_name = 'courses/about.html'

    def get_context_data(self, **kwargs):
        form = StudentForm()
        comments = CourseComment.objects.all().order_by('-created_at')[:3]
        categories = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['categories'] = categories
        context['form'] = form
        context['comments'] = comments
        return context


class ContactTemplateView(TemplateView):
    template_name = 'courses/contact.html'

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['categories'] = categories
        return context


class CategoryDetailView(TemplateView):
    template_name = 'courses/category-detail.html'

    def get_context_data(self, **kwargs):
        category = Category.objects.get(pk=self.kwargs['pk'])
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        courses = Course.objects.filter(category=category)
        context.update({'category': category, 'courses': courses})
        return context


class BaseIndexPage(View):
    def get(self, request, pk):
        categories = Category.objects.all()
        category = Category.objects.get(pk=pk)
        courses = Course.objects.filter(category=category)
        context = {'categories': categories, 'courses': courses}

        return render(request, 'courses/base.html', context)
