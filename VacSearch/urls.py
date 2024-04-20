from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from API.views import ProjectsViewSet, VacanciesViewSet, CurrentRolesView


router = DefaultRouter()
router.register(r'projects', ProjectsViewSet)
router.register(r'vacancies', VacanciesViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/current-roles/', CurrentRolesView.as_view(), name='current-roles')
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))