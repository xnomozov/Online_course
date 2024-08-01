from django.contrib import admin

from courses.models import Course, Category, Video, Student

from import_export.admin import ImportExportModelAdmin


@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Course)
class CourseAdminModel(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'number_of_students', 'price')
    search_fields = ('title', 'courses')
    list_filter = ('price',)


@admin.register(Video)
class VideoAdminModel(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']


@admin.register(Student)
class StudentAdminModel(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ['name']
    list_filter = ('email',)
