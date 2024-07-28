from django.urls import path

from courses import views

urlpatterns = [
    path('index/', views.IndexTemplateView.as_view(), name='index'),
    path('courses/', views.CourseTemplateView.as_view(), name='courses'),
]