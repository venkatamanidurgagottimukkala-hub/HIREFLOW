
from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary')
    search_fields = ('title', 'company', 'location')
    list_filter = ('location', 'company')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'job', 'applied_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('job', 'applied_at')
    readonly_fields = ('applied_at',)
