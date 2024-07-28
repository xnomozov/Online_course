from django.urls import path

from blog import views

urlpatterns = [
    path('blogs/', views.BlogPostListView.as_view(), name='index'),
]