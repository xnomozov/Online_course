from django.urls import path

from courses.views.course import views
from courses.views.authentication import views as auth_views

urlpatterns = [
    path('index/', views.IndexTemplateView.as_view(), name='index'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('about/', views.AboutTemplateView.as_view(), name='about'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_courses'),
    path('contact/', auth_views.ContactView.as_view(), name='contact'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', auth_views.RegisterView.as_view(), name='register'),

    path('activate/<uidb64>/<token>/', auth_views.activate, name='activate'),
]
