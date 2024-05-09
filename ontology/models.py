from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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

class FileUpload(models.Model):
    FILE_TYPES = [
        ('vacancy', 'Vacancy'),
        ('skill', 'Skill'),
        ('ontology', 'Ontology'),
    ]
    FILE_FORMATS = {
        'vacancy': ['.xlsx'],
        'skill': ['.xlsx'],
        'ontology': ['.owx']
    }

    file = models.FileField(upload_to='uploads/')
    description = models.CharField(max_length=255, blank=True)
    tag_type = models.CharField(max_length=50, choices=FILE_TYPES, default='vacancy')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_loaded = models.BooleanField(default=False)
    def clean(self):
        file_extension = self.file.name.split('.')[-1]
        allowed_extensions = self.FILE_FORMATS[self.tag_type]

        if f".{file_extension}" not in allowed_extensions:
            raise ValidationError(
                _(f"Неверный формат для {self.tag_type}. Допустимые форматы: {', '.join(allowed_extensions)}")
            )

    def __str__(self):
        return self.description or self.file.name