from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from API.views import ProjectsViewSet, VacanciesViewSet, SearchVacancyTagView, search_vacancies, SearchSkillTagView, StatsView


router = DefaultRouter()
router.register(r'projects', ProjectsViewSet)
router.register(r'vacancies', VacanciesViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/role_search/', SearchVacancyTagView.as_view(), name='search-roles'),
    path('api/skill_search/', SearchSkillTagView.as_view(), name='search-skills'),
    path('api/search_vacancies/', search_vacancies, name='search_vacancies'),
    path('api/stats/', StatsView.as_view(), name='stats')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))