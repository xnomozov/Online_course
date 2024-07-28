from django.urls import path

from teachers import views

urlpatterns = [
    path('teachers/', views.TeacherListView.as_view(), name='index'),

]