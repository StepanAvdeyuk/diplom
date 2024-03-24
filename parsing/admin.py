from django.contrib import admin
from .models import Heads, Types, Stage, Projects, Vacancies

@admin.register(Heads)
class HeadsModelAdmin(admin.ModelAdmin):
    search_fields = ('head_name', 'head_surname')
    ordering = ['head_surname']

@admin.register(Projects)
class ProjectsModelAdmin(admin.ModelAdmin):
    search_fields = ('project_id', 'project_name')
    ordering = ['project_name']
    list_per_page = 100

admin.site.register(Types)
admin.site.register(Stage)
admin.site.register(Vacancies)

# Register your models here.
