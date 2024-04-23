from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from parsing.models import Projects, Vacancies
from .serializers import ProjectsSerializer, VacanciesSerializer, VacancyTagSerializer
from ontology.models import VacancyTag, VacancyTagVariation
from parsing.models import Roles_in_vacancies


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