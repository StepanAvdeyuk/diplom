from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from API.views import ProjectsViewSet, VacanciesViewSet, CurrentRolesView, SearchVacancyTagView, search_vacancies, SearchSkillTagView


router = DefaultRouter()
router.register(r'projects', ProjectsViewSet)
router.register(r'vacancies', VacanciesViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/role_search/', SearchVacancyTagView.as_view(), name='search-roles'),
    path('api/skill_search/', SearchSkillTagView.as_view(), name='search-skills'),
    path('api/search_vacancies/', search_vacancies, name='search_vacancies'),
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))