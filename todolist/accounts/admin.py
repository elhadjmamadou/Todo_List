from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "due_date", "priority","completed","category","user",)
    list_editable = ("completed", )


admin.site.register(Task,TaskAdmin)