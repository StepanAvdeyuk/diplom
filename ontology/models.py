from django.db import models

class OntologyRoles(models.Model):
    role_tag = models.CharField(max_length=256)

class OntologySkills(models.Model):
    skill_tag = models.CharField(max_length=256)
