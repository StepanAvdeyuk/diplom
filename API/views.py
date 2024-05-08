from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from parsing.models import Projects, Vacancies
from .serializers import ProjectsSerializer, VacanciesSerializer, VacancyTagSerializer, SkillTagSerializer
from ontology.models import VacancyTag, VacancyTagVariation, SkillTag, SkillTagVariation
from parsing.models import Roles_in_vacancies, Skills_in_vacancies
from django.http import JsonResponse
from django.db.models import Count, Sum


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
    # Получаем список названий тегов вакансии и навыков
    vacancy_tag_names = request.GET.getlist('vacancy_tags')
    skill_tag_names = request.GET.getlist('skill_tags')

    try:
        # Инициализируем QuerySet вакансий
        vacancies = Vacancies.objects.all()
        # Фильтрация вакансий по названиям тегов роли
        if vacancy_tag_names:
            vacancies = vacancies.filter(roles_in_vacancies__role_name__name__in=vacancy_tag_names).distinct()
        # Фильтрация по названиям тегов навыков
        if skill_tag_names:
            vacancies = vacancies.filter(skills_in_vacancies__skill_name__name__in=skill_tag_names).distinct()

        # Расчет очков для каждой вакансии
        vacancies_scores = []
        for vacancy in vacancies:
            score = 0
            # Добавляем очки за теги роли
            for role_in_vacancy in vacancy.roles_in_vacancies.all():
                if role_in_vacancy.role_name.name in vacancy_tag_names:
                    score += 50 if role_in_vacancy.priority == 1 else 10 if role_in_vacancy.priority == 2 else 0

            # Добавляем очки за совпадения навыков с приоритетами
            for skill in Skills_in_vacancies.objects.filter(vacancy_id=vacancy):
                if skill.skill_name.name in skill_tag_names:
                    score += {1: 10,
                              2: 7,
                              3: 5,
                              4: 4,
                              5: 2}.get(skill.priority, 0)
            if (score==0) or (score>= 3):
                vacancies_scores.append((vacancy, score))

        # Сортировка вакансий по очкам
        vacancies_scores.sort(key=lambda x: x[1], reverse=True)
        sorted_vacancies = [vac[0] for vac in vacancies_scores]

        # Сериализация отсортированных вакансий
        serializer = VacanciesSerializer(sorted_vacancies, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class StatsView(APIView):
    def get(self, request):
        # Агрегируем количество вакансий по каждому тегу, учитывая vacancy_count
        roles_with_counts = Roles_in_vacancies.objects.values('role_name__annotation', 'role_name__name').annotate(
            count=Sum('vacancy_id__vacancy_count')).order_by('-count')
        skills_with_counts = Skills_in_vacancies.objects.filter(priority__lt=5).values(
            'skill_name__annotation', 'skill_name__name').annotate(
            count=Sum('vacancy_id__vacancy_count')).order_by('-count')
        # Подсчитываем общее количество вакансий
        total_vacancies = Vacancies.objects.aggregate(total=Sum('vacancy_count'))['total']
        # Формируем ответ
        response_data = {
            'total_vacancies': total_vacancies,
            'role_tags': list(roles_with_counts),
            'skill_tags': list(skills_with_counts)
        }
        return Response(response_data)