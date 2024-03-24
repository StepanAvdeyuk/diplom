from django.db import models
from ontology.models import OntologySkills, OntologyRoles


class Heads(models.Model):
    head_email = models.CharField(max_length=256, primary_key=True)
    head_surname = models.CharField(max_length=256)
    head_name = models.CharField(max_length=256)
    head_fathername = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.head_surname} {self.head_name} {self.head_fathername} ({self.head_email})"

    class Meta:
        verbose_name = 'Head'
        verbose_name_plural = 'Heads'


class Types(models.Model):
    type_name = models.CharField(max_length=256, unique=True, primary_key=True)

    def __str__(self):
        return f"{self.type_name}"

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

class Projects(models.Model):
    project_id = models.IntegerField(primary_key=True)
    project_name = models.TextField()
    project_head = models.ForeignKey(to=Heads, on_delete=models.CASCADE)
    project_type = models.ForeignKey(to=Types, on_delete=models.CASCADE)
    project_url = models.TextField()

    def __str__(self):
        return f"{self.project_name} - {self.project_id}"

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class Stage(models.Model):
    stage_id = models.IntegerField(primary_key=True)
    stage_project = models.ForeignKey(to=Projects, on_delete=models.DO_NOTHING)
    stage_name = models.CharField(max_length=256)
    stage_status = models.IntegerField(null=False)
    date = models.CharField(max_length=256, null=True)
    sessionStartDate = models.CharField(max_length=256, null=True)
    sessionEndDate = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f"{self.stages_name}"

    class Meta:
        verbose_name = 'Stage'
        verbose_name_plural = 'Stages'


class Roles(models.Model):
    role_id = models.IntegerField(unique=True, primary_key=True)
    role_name = models.ForeignKey(to=OntologyRoles, on_delete=models.CASCADE)


class Vacancies(models.Model):
    vacancy_id = models.IntegerField(primary_key=True, unique=True)
    vacancy_name = models.TextField()
    vacancy_project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    vacancy_disciplines = models.TextField()
    vacancy_additionally = models.TextField()
    vacancy_count = models.IntegerField(null=False)

    # vacancy_role = models.ForeignKey(to = Roles, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vacancy_name} - {self.vacancy_project_id}"

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'


class Skills(models.Model):
    skill_id = models.IntegerField(unique=True, primary_key=True)
    skill_name = models.ForeignKey(to=OntologySkills, on_delete=models.CASCADE)


class Skills_in_vacancies(models.Model):
    vacancy_name = models.ForeignKey(to=Vacancies, on_delete=models.CASCADE)
    skill_name = models.ForeignKey(to=Skills, on_delete=models.CASCADE)
    obligation = models.CharField(max_length=256,
                                  choices=[('disciplines', 'disciplines'), ('additionally', 'additionally')])
