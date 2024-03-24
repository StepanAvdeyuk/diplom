# Generated by Django 5.0.2 on 2024-02-24 21:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ontology', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heads',
            fields=[
                ('head_email', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('head_surname', models.CharField(max_length=256)),
                ('head_name', models.CharField(max_length=256)),
                ('head_fathername', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Head',
                'verbose_name_plural': 'Heads',
            },
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('type_name', models.CharField(max_length=256, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
            },
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('project_id', models.IntegerField(primary_key=True, serialize=False)),
                ('project_name', models.TextField()),
                ('project_url', models.TextField()),
                ('project_head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsing.heads')),
                ('project_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsing.types')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('role_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('role_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ontology.ontologyroles')),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('skill_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('skill_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ontology.ontologyskills')),
            ],
        ),
        migrations.CreateModel(
            name='Stages',
            fields=[
                ('stage_id', models.IntegerField(primary_key=True, serialize=False)),
                ('stage_name', models.CharField(max_length=256)),
                ('stage_status', models.IntegerField()),
                ('date', models.CharField(max_length=256, null=True)),
                ('sessionStartDate', models.CharField(max_length=256, null=True)),
                ('sessionEndDate', models.CharField(max_length=256, null=True)),
                ('stage_project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='parsing.projects')),
            ],
            options={
                'verbose_name': 'Stage',
                'verbose_name_plural': 'Stages',
            },
        ),
        migrations.CreateModel(
            name='Vacancies',
            fields=[
                ('vacancy_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('vacancy_name', models.TextField()),
                ('vacancy_disciplines', models.TextField()),
                ('vacancy_additionally', models.TextField()),
                ('vacancy_count', models.IntegerField()),
                ('vacancy_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsing.projects')),
            ],
            options={
                'verbose_name': 'Vacancy',
                'verbose_name_plural': 'Vacancies',
            },
        ),
        migrations.CreateModel(
            name='Skills_in_vacancies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obligation', models.CharField(choices=[('disciplines', 'disciplines'), ('additionally', 'additionally')], max_length=256)),
                ('skill_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsing.skills')),
                ('vacancy_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsing.vacancies')),
            ],
        ),
    ]
