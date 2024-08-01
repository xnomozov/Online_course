from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from teachers.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('full_name', 'email', 'rating')
    search_fields = ('full_name', 'email', 'rating')
    list_filter = ('full_name', 'rating')


