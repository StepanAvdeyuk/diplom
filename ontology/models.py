from django.db import models

class ComplexVacancyTag(models.Model):
    phrase = models.CharField(max_length=100, unique=True, primary_key=True)

class VacancyTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    annotation = models.CharField(max_length=100, null=True)

class VacancyTagVariation(models.Model):
    tag = models.ForeignKey(to=VacancyTag, related_name='variations', on_delete=models.CASCADE)
    variation = models.CharField(max_length=100)

class ComplexSkillTag(models.Model):
    phrase = models.CharField(max_length=100, unique=True, primary_key=True)

class SkillTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    annotation = models.CharField(max_length=100, null=True)

class SkillTagVariation(models.Model):
    tag = models.ForeignKey(to=SkillTag, related_name='variations', on_delete=models.CASCADE)
    variation = models.CharField(max_length=100)