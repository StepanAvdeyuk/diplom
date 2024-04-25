import pandas as pd
import string
from django.db import transaction
from .models import ComplexVacancyTag, VacancyTag, VacancyTagVariation, ComplexSkillTag, SkillTag, SkillTagVariation
from parsing.models import Vacancies, Roles_in_vacancies, Skills_in_vacancies
from ontology.ontology import OntologyManager

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
vacancy_importer = DataImporter(filepath='ontology/non_skill_variations.xlsx', tag_type='vacancy')
vacancy_importer.read_variations()

# Для навыков
skill_importer = DataImporter(filepath='ontology/skill_variations.xlsx', tag_type='skill')
skill_importer.read_variations()


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


def check_vacancy_tags():
    onto = OntologyManager.get_instance().get_ontology()
    all_skills_data = {}
    original_skills_data = {}

    # Сначала собираем исходные данные о навыках
    for siv in Skills_in_vacancies.objects.all():
        skill_name = siv.skill_name.name.lower()
        vacancy_id = siv.vacancy_id_id
        original_skills_data.setdefault(vacancy_id, set()).add(skill_name)

    # Сбор информации о навыках для каждой роли в каждой вакансии
    for riv in Roles_in_vacancies.objects.all():
        role_name = riv.role_name.name
        vacancy_id = riv.vacancy_id_id
        role_instance = next((inst for inst in onto.role.instances() if inst.name == role_name), None)

        if role_instance:
            print(f"Тег вакансии '{vacancy_id}' соответствует инстансу '{role_instance}' класса онтологии: role")
            all_skills_data.setdefault(vacancy_id, set()).update(get_skills_from_ontology(role_instance))
        else:
            print(f"Тег вакансии '{vacancy_id}' не найден в онтологии как role. Поиск возможных ролей...")
            if vacancy_id in original_skills_data:
                most_likely_role = infer_roles_from_skills(vacancy_id, original_skills_data[vacancy_id], onto)
                if most_likely_role:
                    all_skills_data.setdefault(vacancy_id, set()).update(get_skills_from_ontology(most_likely_role))

    # Обработка и обновление навыков в базе данных
    update_vacancy_skills(all_skills_data, original_skills_data)


def infer_roles_from_skills(vacancy_id, skills, onto):
    possible_roles = {}
    # Исследовать все роли в онтологии
    for role_class in [onto.role]:
        for instance in role_class.instances():
            role_skills = {skill.name.lower() for skill in instance.includes}
            if skills.intersection(role_skills):
                possible_roles[instance] = role_skills

    # Определить наилучшее соответствие, если возможно
    best_match = determine_best_match(possible_roles, skills)
    if best_match:
        print(f"Наилучшее соответствие для вакансии {vacancy_id} найдено: {best_match}.")
        update_role_in_vacancy(vacancy_id, best_match)
        return best_match  # Возвращаем наиболее вероятную роль
    else:
        print(f"Ни одно соответствие для вакансии {vacancy_id} не найдено.")
        return None

def update_role_in_vacancy(vacancy_id, best_match):
    # Получение или создание объекта VacancyTag для наилучшего соответствия
    vacancy_tag, _ = VacancyTag.objects.get_or_create(name=best_match.name)

    # Попытка найти существующую роль в вакансии
    try:
        role_in_vacancy = Roles_in_vacancies.objects.get(vacancy_id_id=vacancy_id, role_name=vacancy_tag)
        print(f"Роль для вакансии {vacancy_id} уже существует и будет обновлена.")
    except Roles_in_vacancies.DoesNotExist:
        role_in_vacancy = Roles_in_vacancies(vacancy_id_id=vacancy_id, role_name=vacancy_tag)
        print(f"Создана новая роль для вакансии {vacancy_id}.")
    except Roles_in_vacancies.MultipleObjectsReturned:
        print(f"Найдено несколько ролей для вакансии {vacancy_id}, требуется вмешательство.")
        return

    role_in_vacancy.save()  # Сохраняем или обновляем объект

def determine_best_match(possible_roles, skills):
    # Определение наилучшего соответствия роли навыкам
    best_match = None
    max_intersection = 0
    for role, role_skills in possible_roles.items():
        intersection_size = len(skills.intersection(role_skills))
        if intersection_size > max_intersection:
            max_intersection = intersection_size
            best_match = role
    return best_match

def get_skills_from_ontology(role_instance):
    # Возвращает навыки из онтологии для данной роли
    return {skill.name.lower() for skill in role_instance.includes}

def update_vacancy_skills(all_skills_data, original_skills_data):
    with transaction.atomic():
        for vacancy_id, skills in all_skills_data.items():
            original_skills = original_skills_data.get(vacancy_id, set())
            for skill_name in skills:
                priority = determine_priority(skill_name, original_skills, skills)
                if priority:  # Убедитесь, что приоритет был успешно определен
                    skill_tag, _ = SkillTag.objects.get_or_create(name=skill_name)
                    Skills_in_vacancies.objects.update_or_create(
                        vacancy_id_id=vacancy_id,
                        skill_name=skill_tag,
                        defaults={'priority': priority}
                    )
                    print(f"Навык '{skill_name}' для вакансии '{vacancy_id}' обновлен до приоритета {priority}")
def determine_priority(skill_name, original_skills, ontology_skills):

    skill_in_original = skill_name in original_skills
    skill_in_ontology = skill_name in ontology_skills

    if skill_in_original and skill_in_ontology:
        return 1  # Навык присутствует в исходных тегах и онтологии
    elif skill_in_original and not skill_in_ontology:
        return 2  # Навык присутствует только в исходных тегах
    elif skill_in_ontology and not skill_in_original:
        return 3  # Навык присутствует только в онтологии