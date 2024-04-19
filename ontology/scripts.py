import pandas as pd
import string
from django.db import transaction
from .models import ComplexTag, VacancyTag, VacancyTagVariation
from parsing.models import Vacancies, Roles_in_vacancies

def read_vacancies_variations(filepath):
    df = pd.read_excel(filepath, header=None)

    complex_tags = [tag.strip() for tag in df.iloc[:, 0].dropna()]
    with transaction.atomic():
        for tag in complex_tags:
            ComplexTag.objects.get_or_create(phrase=tag)

    for col in range(1, df.shape[1]):
        tag_name = df.iloc[0, col]
        if pd.notnull(tag_name):
            tag_name = tag_name.strip()
            tag, created = VacancyTag.objects.get_or_create(name=tag_name)
            variations = df.iloc[1:, col].dropna().apply(str.strip).tolist()
            with transaction.atomic():
                for variation in variations:
                    VacancyTagVariation.objects.get_or_create(tag=tag, variation=variation)

def get_complex_tags():
    return [tag.phrase for tag in ComplexTag.objects.all()]

def get_vacancies_tags_dict():
    tags_dict = {}
    for tag in VacancyTag.objects.all():
        tags_dict[tag.name] = [variation.variation for variation in tag.variations.all()]
    return tags_dict

def normalize_text(text, complex_tags):
    text = text.lower()
    text = text.replace('/', ' ')
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
    complex_tags = get_complex_tags()
    tags_dict = get_vacancies_tags_dict()
    all_vacancies = Vacancies.objects.all()

    for vacancy in all_vacancies:
        normalized_name = normalize_text(vacancy.vacancy_name, complex_tags)
        matched_tags = match_tags(normalized_name, tags_dict)

        if not matched_tags:
            matched_tags.append('разное')

        with transaction.atomic():
            for tag_name in matched_tags:
                tag, _ = VacancyTag.objects.get_or_create(name=tag_name)
                Roles_in_vacancies.objects.get_or_create(vacancy_id=vacancy, role_name=tag)