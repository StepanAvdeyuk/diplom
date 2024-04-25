from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from parsing.models import Projects, Vacancies
from .serializers import ProjectsSerializer, VacanciesSerializer, VacancyTagSerializer, SkillTagSerializer
from ontology.models import VacancyTag, VacancyTagVariation, SkillTag, SkillTagVariation
from parsing.models import Roles_in_vacancies, Skills_in_vacancies
from django.http import JsonResponse


def create_model_viewset(model, serializer):
    class ModelViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = model.objects.all()
        serializer_class = serializer
    return ModelViewSet

ProjectsViewSet = create_model_viewset(Projects, ProjectsSerializer)
VacanciesViewSet = create_model_viewset(Vacancies, VacanciesSerializer)
# Create your views here.

class CurrentRolesView(APIView):
    def get(self, request):
        role_ids = Roles_in_vacancies.objects.values_list('role_name_id', flat=True).distinct()
        roles = VacancyTag.objects.filter(id__in=role_ids)
        serializer = VacancyTagSerializer(roles, many=True)
        return Response(serializer.data)

class SearchVacancyTagView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')  # Получаем параметр запроса `q`
        if query:
            # Ищем совпадения в вариациях
            variations = VacancyTagVariation.objects.filter(variation__icontains=query)
            # Получаем уникальные теги, связанные с найденными вариациями
            # tags = VacancyTag.objects.filter(
            #     variations__in=variations,
            #     id__in=Roles_in_vacancies.objects.values_list('role_name_id', flat=True).distinct()
            # ).distinct()
            tags = VacancyTag.objects.filter(variations__in=variations).distinct()
        else:
            # Если запрос пустой, возвращаем все теги
            # tags = VacancyTag.objects.filter(
            #     id__in=Roles_in_vacancies.objects.values_list('role_name_id', flat=True).distinct()
            # )
            tags = VacancyTag.objects.all()
        serializer = VacancyTagSerializer(tags, many=True)
        return Response(serializer.data)

class SearchSkillTagView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')  # Получаем параметр запроса `q`
        if query:
            # Ищем совпадения в вариациях
            variations = SkillTagVariation.objects.filter(variation__icontains=query)
            # Получаем уникальные теги, связанные с найденными вариациями
            # tags = VacancyTag.objects.filter(
            #     variations__in=variations,
            #     id__in=Roles_in_vacancies.objects.values_list('role_name_id', flat=True).distinct()
            # ).distinct()
            tags = SkillTag.objects.filter(variations__in=variations).distinct()
        else:
            # Если запрос пустой, возвращаем все теги
            # tags = VacancyTag.objects.filter(
            #     id__in=Roles_in_vacancies.objects.values_list('role_name_id', flat=True).distinct()
            # )
            tags = SkillTag.objects.all()
        serializer = SkillTagSerializer(tags, many=True)
        return Response(serializer.data)

def search_vacancies(request):
    # Получаем список ID тегов вакансии
    vacancy_tag_ids = request.GET.getlist('vacancy_tags')
    # Получаем список ID тегов навыков
    skill_tag_ids = request.GET.getlist('skill_tags')

    try:
        # Инициализируем QuerySet вакансий
        vacancies = Vacancies.objects.all()

        # Фильтрация вакансий по тегам роли, если указаны
        if vacancy_tag_ids:
            vacancies = vacancies.filter(
                roles_in_vacancies__role_name_id__in=vacancy_tag_ids
            ).distinct()

        # Дополнительная фильтрация по тегам навыков, если указаны
        if skill_tag_ids:
            vacancies = vacancies.filter(
                skills_in_vacancies__skill_name_id__in=skill_tag_ids
            ).distinct()

        # Сериализация данных о вакансиях
        serializer = VacanciesSerializer(vacancies, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
