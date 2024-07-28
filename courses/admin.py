from django.contrib import admin

from courses.models import Course, Category


@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Course)
class CourseAdminModel(admin.ModelAdmin):
    list_display = ('title', 'number_of_students', 'price')
    search_fields = ('title', 'teachers')
    list_filter = ('price',)
