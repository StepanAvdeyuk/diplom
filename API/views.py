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

# class SearchVacancyTagView(APIView):
#     def get(self, request):
#         query = request.query_params.get('q', '')  # Получаем параметр запроса `q`
#         if query:
#             # Ищем совпадения в вариациях
#             variations = VacancyTagVariation.objects.filter(variation__icontains=query)
#             # Получаем уникальные теги, связанные с найденными вариациями
#             # tags = VacancyTag.objects.filter(
#             #     variations__in=variations,
#             #     id__in=Roles_in_vacancies.objects.values_list('role_name_id', flat=True).distinct()
#             # ).distinct()
#             tags = VacancyTag.objects.filter(variations__in=variations).distinct()
#         else:
#             # Если запрос пустой, возвращаем все теги
#             # tags = VacancyTag.objects.filter(
#             #     id__in=Roles_in_vacancies.objects.values_list('role_name_id', flat=True).distinct()
#             # )
#             tags = VacancyTag.objects.all()
#         serializer = VacancyTagSerializer(tags, many=True)
#         return Response(serializer.data)

class SearchVacancyTagView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if query:
            starts_with_tags = VacancyTag.objects.filter(
                variations__variation__istartswith=query
            ).distinct()
            contains_tags = VacancyTag.objects.filter(
                variations__variation__icontains=query
            ).distinct().exclude(id__in=starts_with_tags.values_list('id', flat=True))

            tags = list(starts_with_tags) + list(contains_tags)
            tags = sorted(tags, key=lambda tag: len(tag.annotation))
        else:
            tags = VacancyTag.objects.all()

        # Sort the tags by the length of their names
        tags = sorted(tags, key=lambda tag: len(tag.name))

        serializer = VacancyTagSerializer(tags, many=True)
        return Response(serializer.data)

# class SearchSkillTagView(APIView):
#     def get(self, request):
#         query = request.query_params.get('q', '')  # Получаем параметр запроса `q`
#         if query:
#             # Ищем совпадения в вариациях
#             variations = SkillTagVariation.objects.filter(variation__icontains=query)
#             # Получаем уникальные теги, связанные с найденными вариациями
#             # tags = VacancyTag.objects.filter(
#             #     variations__in=variations,
#             #     id__in=Roles_in_vacancies.objects.values_list('role_name_id', flat=True).distinct()
#             # ).distinct()
#             tags = SkillTag.objects.filter(variations__in=variations).distinct()
#         else:
#             # Если запрос пустой, возвращаем все теги
#             # tags = VacancyTag.objects.filter(
#             #     id__in=Roles_in_vacancies.objects.values_list('role_name_id', flat=True).distinct()
#             # )
#             tags = SkillTag.objects.all()
#         serializer = SkillTagSerializer(tags, many=True)
#         return Response(serializer.data)

class SearchSkillTagView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if query:
            starts_with_tags = SkillTag.objects.filter(
                variations__variation__istartswith=query
            ).distinct()
            contains_tags = SkillTag.objects.filter(
                variations__variation__icontains=query
            ).distinct().exclude(id__in=starts_with_tags.values_list('id', flat=True))

            tags = list(starts_with_tags) + list(contains_tags)
            tags = sorted(tags, key=lambda tag: len(tag.annotation))
        else:
            tags = SkillTag.objects.all()

        serializer = SkillTagSerializer(tags, many=True)
        return Response(serializer.data)


def search_vacancies(request):
    # Получаем список ID тегов вакансии и навыков
    vacancy_tag_ids = [int(id) for id in request.GET.getlist('vacancy_tags')]
    skill_tag_ids = [int(id) for id in request.GET.getlist('skill_tags')]

    try:
        # Инициализируем QuerySet вакансий
        vacancies = Vacancies.objects.all()
        # Фильтрация вакансий по тегам роли
        if vacancy_tag_ids:
            vacancies = vacancies.filter(roles_in_vacancies__role_name_id__in=vacancy_tag_ids).distinct()
        # Фильтрация по тегам навыков
        if skill_tag_ids:
            vacancies = vacancies.filter(skills_in_vacancies__skill_name_id__in=skill_tag_ids).distinct()
        # Расчет очков для каждой вакансии
        vacancies_scores = []
        for vacancy in vacancies:
            score = 0
            # Добавляем очки за теги роли
            for role_in_vacancy in vacancy.roles_in_vacancies.all():
                if role_in_vacancy.role_name_id in vacancy_tag_ids:
                    if role_in_vacancy.priority == 1:
                        score += 50
                    elif role_in_vacancy.priority == 2:
                        score += 10

            # Добавляем очки за совпадения навыков с приоритетами
            for skill in Skills_in_vacancies.objects.filter(vacancy_id=vacancy):
                if skill.skill_name_id in skill_tag_ids:
                    if skill.priority == 1:
                        score += 10
                    elif skill.priority == 2:
                        score += 7
                    elif skill.priority == 3:
                        score += 5
                    elif skill.priority == 4:
                        score += 4
                    elif skill.priority == 5:
                        score += 2

            vacancies_scores.append((vacancy, score))

        # Сортировка вакансий по очкам
        vacancies_scores.sort(key=lambda x: x[1], reverse=True)
        sorted_vacancies = [vac[0] for vac in vacancies_scores]

        # Сериализация отсортированных вакансий
        serializer = VacanciesSerializer(sorted_vacancies, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)