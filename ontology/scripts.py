import pandas as pd
import string
from django.db import transaction
from .models import ComplexVacancyTag, VacancyTag, VacancyTagVariation, ComplexSkillTag, SkillTag, SkillTagVariation
from parsing.models import Vacancies, Roles_in_vacancies, Skills_in_vacancies


class DataImporter:
    def __init__(self, filepath, tag_type='vacancy'):
        self.filepath = filepath
        self.tag_type = tag_type

        # Сопоставление типов тегов с моделями
        if tag_type == 'vacancy':
            self.complex_tag_model = ComplexVacancyTag
            self.tag_model = VacancyTag
            self.tag_variation_model = VacancyTagVariation
        elif tag_type == 'skill':
            self.complex_tag_model = ComplexSkillTag
            self.tag_model = SkillTag
            self.tag_variation_model = SkillTagVariation

    def read_variations(self):
        # Очистка предыдущих данных
        self.complex_tag_model.objects.all().delete()
        self.tag_model.objects.all().delete()
        self.tag_variation_model.objects.all().delete()

        # Чтение файла Excel
        df = pd.read_excel(self.filepath, header=None)

        # Чтение сложных тегов из первого столбца
        complex_tags = [tag.strip() for tag in df.iloc[:, 0].dropna()]
        with transaction.atomic():
            for tag in complex_tags:
                self.complex_tag_model.objects.get_or_create(phrase=tag)

        # Обработка тегов и вариаций
        for col in range(1, df.shape[1]):
            tag_name = df.iloc[0, col]  # Тег находится в первой строке
            annotation = df.iloc[1, col]  # Аннотация находится во второй строке
            if pd.notnull(tag_name):
                annotation = annotation.strip() if pd.notnull(annotation) else ''
                tag, created = self.tag_model.objects.get_or_create(
                    name=tag_name,
                    defaults={'annotation': annotation})
                variations = df.iloc[2:, col].dropna().apply(str.strip).tolist()
                with transaction.atomic():
                    for variation in variations:
                        self.tag_variation_model.objects.get_or_create(tag=tag, variation=variation)

# Для вакансий
# vacancy_importer = DataImporter(filepath='ontology/non_skill_variations.xlsx', tag_type='vacancy')
# vacancy_importer.read_variations()
#
# # Для навыков
# skill_importer = DataImporter(filepath='ontology/skill_variations.xlsx', tag_type='skill')
# skill_importer.read_variations()


def get_complex_vacancy_tags():
    return [tag.phrase for tag in ComplexVacancyTag.objects.all()]

def get_complex_skill_tags():
    return [tag.phrase for tag in ComplexSkillTag.objects.all()]


def get_vacancies_tags_dict():
    tags_dict = {}
    for tag in VacancyTag.objects.all():
        tags_dict[tag.name] = [variation.variation for variation in tag.variations.all()]
    return tags_dict

def get_skills_tags_dict():
    tags_dict = {}
    for tag in SkillTag.objects.all():
        tags_dict[tag.name] = [variation.variation for variation in tag.variations.all()]
    return tags_dict

def normalize_text(text, complex_tags):
    text = text.lower()
    text = text.replace('/', ' ').replace('\\', ' ')
    table = str.maketrans('', '', string.punctuation.translate(
        str.maketrans('', '', '+-._#')))

    # Обработка сложных тегов
    for tag in complex_tags:
        if tag in text:
            text = text.replace(tag, tag.replace(' ', '_'))

    normalized_text = [word.translate(table).replace('_', ' ') for word in text.split()]
    return normalized_text


def match_tags(vacancy_text, tags_dict):
    matched_tags = []
    for word in vacancy_text:
        for tag, variations in tags_dict.items():
            if word in variations and tag not in matched_tags:
                matched_tags.append(tag)
    return matched_tags


def tag_vacancies():
    Roles_in_vacancies.objects.all().delete()
    Skills_in_vacancies.objects.all().delete()
    complex_vacancy_tags = get_complex_vacancy_tags()
    complex_skill_tags = get_complex_skill_tags()
    vacancy_tags_dict = get_vacancies_tags_dict()
    skill_tags_dict = get_skills_tags_dict()
    all_vacancies = Vacancies.objects.all()
    total_vacancies = len(all_vacancies)
    tagged_vacancies_count = 0
    tagged_skills_count = 0


    for vacancy in all_vacancies:
        disciplines_info = vacancy.vacancy_disciplines
        additional_info = vacancy.vacancy_additionally
        skills = f"{disciplines_info} {additional_info}"

        normalized_name = normalize_text(vacancy.vacancy_name, complex_vacancy_tags)
        matched_tags = match_tags(normalized_name, vacancy_tags_dict)

        if not matched_tags:
            matched_tags.append('разное')
        else:
            tagged_vacancies_count += 1

        with transaction.atomic():
            for tag_name in matched_tags:
                tag, _ = VacancyTag.objects.get_or_create(name=tag_name)
                Roles_in_vacancies.objects.get_or_create(vacancy_id=vacancy, role_name=tag)

        normalized_skills = normalize_text(skills, complex_skill_tags)
        matched_skills = match_tags(normalized_skills, skill_tags_dict)

        if matched_skills:
            tagged_skills_count += 1

        with transaction.atomic():
            for tag_name in matched_skills:
                tag, _ = SkillTag.objects.get_or_create(name=tag_name)
                Skills_in_vacancies.objects.get_or_create(vacancy_id=vacancy, skill_name=tag, priority=2)

    vacancy_tag_coverage = (tagged_vacancies_count / total_vacancies) * 100
    skill_tag_coverage = (tagged_skills_count / total_vacancies) * 100

    print(f"Покрытие ролей: {vacancy_tag_coverage:.2f}%")
    print(f"Покрытие навыков: {skill_tag_coverage:.2f}%")