from rest_framework import serializers
from parsing.models import Stage, Projects, Vacancies


def create_model_serializer(Model):
    class ModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = Model
            fields = '__all__'

    return ModelSerializer


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['stage_name', 'stage_status', 'date', 'sessionStartDate', 'sessionEndDate']

class HeadField(serializers.Field):
    def to_representation(self, obj):
        return {
            'email': obj.head_email,
            'full_name': f"{obj.head_surname} {obj.head_name} {obj.head_fathername}"
        }

class VacanciesSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(source='vacancy_project.project_id')
    project_name = serializers.CharField(source='vacancy_project.project_name')
    project_type = serializers.CharField(source='vacancy_project.project_type.type_name')
    project_head = HeadField(source='vacancy_project.project_head')
    project_stage = StageSerializer(source='vacancy_project.stage_set', many=True)
    project_url = serializers.CharField(source='vacancy_project.project_url')

    class Meta:
        model = Vacancies
        fields = ['vacancy_id', 'vacancy_name', 'project_id', 'project_name', 'project_type', 'project_head', 'project_stage',
                  'project_url', 'vacancy_disciplines', 'vacancy_additionally']

ProjectsSerializer = create_model_serializer(Projects)
