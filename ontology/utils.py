import pandas as pd
from owlready2 import get_ontology, onto_path
from django.db import transaction
from .models import ComplexVacancyTag, VacancyTag, VacancyTagVariation, ComplexSkillTag, SkillTag, SkillTagVariation, FileUpload
import os
from ontology.scripts import tag_vacancies, check_vacancy_tags

class OntologyManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.onto = None

    def load_ontology(self, file_path):
        # Clean up existing ontology
        if self.onto:
            self.onto.destroy()

        onto_path.append(os.path.dirname(file_path))
        self.onto = get_ontology(f"file://{file_path}")
        self.onto.load()

    def get_ontology(self):
        return self.onto

class DataImporter:
    def __init__(self, filepath, tag_type='vacancy'):
        self.filepath = filepath
        self.tag_type = tag_type

        if tag_type == 'vacancy':
            self.complex_tag_model = ComplexVacancyTag
            self.tag_model = VacancyTag
            self.tag_variation_model = VacancyTagVariation
        elif tag_type == 'skill':
            self.complex_tag_model = ComplexSkillTag
            self.tag_model = SkillTag
            self.tag_variation_model = SkillTagVariation

    def read_variations(self):
        self.complex_tag_model.objects.all().delete()
        self.tag_model.objects.all().delete()
        self.tag_variation_model.objects.all().delete()

        df = pd.read_excel(self.filepath, header=None)

        complex_tags = [tag.strip() for tag in df.iloc[:, 0].dropna()]
        with transaction.atomic():
            for tag in complex_tags:
                self.complex_tag_model.objects.get_or_create(phrase=tag)

        for col in range(1, df.shape[1]):
            tag_name = df.iloc[0, col]
            annotation = df.iloc[1, col]
            if pd.notnull(tag_name):
                annotation = annotation.strip() if pd.notnull(annotation) else ''
                tag, _ = self.tag_model.objects.get_or_create(name=tag_name, defaults={'annotation': annotation})
                variations = df.iloc[2:, col].dropna().apply(str.strip).tolist()
                with transaction.atomic():
                    for variation in variations:
                        self.tag_variation_model.objects.get_or_create(tag=tag, variation=variation)

def process_file(file_upload):
    file_extension = file_upload.file.name.split('.')[-1]
    allowed_extensions = FileUpload.FILE_FORMATS[file_upload.tag_type]

    if f".{file_extension}" not in allowed_extensions:
        raise ValueError(f"Неверный формат для {file_upload.tag_type}. Допустимые форматы: {', '.join(allowed_extensions)}")

    # Process the file based on the type
    if file_upload.tag_type == 'vacancy':
        vacancy_importer = DataImporter(filepath=file_upload.file.path, tag_type='vacancy')
        vacancy_importer.read_variations()
        tag_vacancies()
        check_vacancy_tags()
    elif file_upload.tag_type == 'skill':
        skill_importer = DataImporter(filepath=file_upload.file.path, tag_type='skill')
        skill_importer.read_variations()
        tag_vacancies()
        check_vacancy_tags()
    elif file_upload.tag_type == 'ontology':
        FileUpload.objects.filter(tag_type='ontology').update(last_loaded=False)
        file_upload.last_loaded = True
        file_upload.save()
        ontology_manager = OntologyManager.get_instance()
        ontology_manager.load_ontology(file_upload.file.path)
        print(f"Загружена онтология из {file_upload.file.path}")