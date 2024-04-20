from django.db import models


class ComplexTag(models.Model):
    phrase = models.CharField(max_length=100, unique=True, primary_key=True)

class VacancyTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

class VacancyTagVariation(models.Model):
    tag = models.ForeignKey(to=VacancyTag, related_name='variations', on_delete=models.CASCADE)
    variation = models.CharField(max_length=100)
