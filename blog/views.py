from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from blog.models import Blog


# Create your views here.
class BlogPostListView(TemplateView):
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all()
        return context
