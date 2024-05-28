from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from parsing.models import Projects, Vacancies
from .serializers import ProjectsSerializer, VacanciesSerializer, VacancyTagSerializer, SkillTagSerializer
from ontology.models import VacancyTag, SkillTag, FileUpload
from parsing.models import Roles_in_vacancies, Skills_in_vacancies
from django.db.models import Sum, Prefetch
from ontology.utils import OntologyManager


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
        role_tag = self.get_role_tags_from_ontology()

        if query:
            starts_with_tags = VacancyTag.objects.filter(
                name__in=role_tag,
                variations__variation__istartswith=query
            ).distinct()
            contains_tags = VacancyTag.objects.filter(
                name__in=role_tag,
                variations__variation__icontains=query
            ).distinct().exclude(id__in=starts_with_tags.values_list('id', flat=True))

            tags = list(starts_with_tags) + list(contains_tags)
            tags = sorted(tags, key=lambda tag: len(tag.annotation))
        else:
            tags = VacancyTag.objects.filter(name__in=role_tag)

        tags = sorted(tags, key=lambda tag: len(tag.name))

        serializer = VacancyTagSerializer(tags, many=True)
        return Response(serializer.data)

    def get_role_tags_from_ontology(self):
        manager = OntologyManager.get_instance()
        ontology = manager.get_ontology()
        if ontology is None:
            last_loaded_file = FileUpload.objects.filter(tag_type='ontology', last_loaded=True).first()
            if last_loaded_file:
                manager.load_ontology(last_loaded_file.file.path)

        try:
            ontology_classes = [ontology.role, ontology.baserole]
            role_tags = set()

            for role_class in ontology_classes:
                for instance in role_class.instances():
                    role_tags.add(instance.name)

            return role_tags
        except AttributeError as e:
            print(f"Ошибка при доступе к атрибутам онтологии: {e}")
            return set()

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


@api_view(['GET'])
def search_vacancies(request):
    vacancy_tag_names = request.GET.getlist('vacancy_tags')
    skill_tag_names = request.GET.getlist('skill_tags')

    try:
        if not vacancy_tag_names and not skill_tag_names:
            vacancies = Vacancies.objects.all()
            serializer = VacanciesSerializer(vacancies, many=True)
            return Response(serializer.data)

        # Подготавливаем запросы для prefetch_related
        role_prefetch = Prefetch('roles_in_vacancies', queryset=Roles_in_vacancies.objects.filter(role_name__name__in=vacancy_tag_names))
        skill_prefetch = Prefetch('skills_in_vacancies', queryset=Skills_in_vacancies.objects.filter(skill_name__name__in=skill_tag_names))

        # Используем distinct и prefetch_related для оптимизации
        vacancies = Vacancies.objects.all().prefetch_related(role_prefetch, skill_prefetch).distinct()

        vacancies_scores = []
        for vacancy in vacancies:
            score = 0
            for role in vacancy.roles_in_vacancies.all():
                score += 50 if role.priority == 1 else 10

            for skill in vacancy.skills_in_vacancies.all():
                score += {1: 10, 2: 7, 3: 5, 4: 4, 5: 2}.get(skill.priority, 0)

            if score > 2:
                vacancies_scores.append((vacancy, score))

        vacancies_scores.sort(key=lambda x: x[1], reverse=True)
        sorted_vacancies = [vac[0] for vac in vacancies_scores]
        serializer = VacanciesSerializer(sorted_vacancies, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StatsView(APIView):
    def get(self, request):
        roles_with_counts = Roles_in_vacancies.objects.values('role_name__annotation', 'role_name__name').annotate(
            count=Sum('vacancy_id__vacancy_count')).order_by('-count')
        skills_with_counts = Skills_in_vacancies.objects.filter(priority__lt=5).values(
            'skill_name__annotation', 'skill_name__name').annotate(
            count=Sum('vacancy_id__vacancy_count')).order_by('-count')
        total_vacancies = Vacancies.objects.aggregate(total=Sum('vacancy_count'))['total']
        response_data = {
            'total_vacancies': total_vacancies,
            'role_tags': list(roles_with_counts),
            'skill_tags': list(skills_with_counts)
        }
        return Response(response_data)

