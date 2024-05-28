import string, os
from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, Doc
from django.db import transaction
from .models import ComplexVacancyTag, VacancyTag, ComplexSkillTag, SkillTag
from parsing.models import Vacancies, Roles_in_vacancies, Skills_in_vacancies
from ontology.models import FileUpload
from ontology.utils import OntologyManager

# Инициализация компонентов Natasha
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

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
    table = str.maketrans('', '', string.punctuation.translate(
        str.maketrans('', '', '+-_#/.')))
    text = text.translate(table).replace('-', ' ').replace('/', ' ').replace('.',' ')

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    for token in doc.tokens:
        token.lemmatize(morph_vocab)

    lemmatized_text = ''.join([token.lemma if token.lemma in '+-_#' else ' ' + token.lemma for token in doc.tokens]).strip()


    # Обработка сложных тегов
    for tag in complex_tags:
        if tag in lemmatized_text:
            lemmatized_text = lemmatized_text.replace(tag, tag.replace(' ', '_'))

    normalized_text = [word.translate(table).replace('_', ' ') for word in lemmatized_text.split()]

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

        normalized_name = normalize_text(vacancy.vacancy_name, complex_vacancy_tags)
        matched_tags = match_tags(normalized_name, vacancy_tags_dict)

        if not matched_tags:
            matched_tags.append('other')
        else:
            tagged_vacancies_count += 1

        with transaction.atomic():
            for tag_name in matched_tags:
                tag, _ = VacancyTag.objects.get_or_create(name=tag_name)
                Roles_in_vacancies.objects.get_or_create(vacancy_id=vacancy, role_name=tag, priority=1)

        normalized_disciplines_skills = normalize_text(disciplines_info, complex_skill_tags)
        normalized_additionally_skills = normalize_text(additional_info, complex_skill_tags)
        matched_disciplines_skills = match_tags(normalized_disciplines_skills, skill_tags_dict)
        matched_additionally_skills = match_tags(normalized_additionally_skills, skill_tags_dict)


        with transaction.atomic():
            for tag_name in matched_disciplines_skills:
                tag, _ = SkillTag.objects.get_or_create(name=tag_name)
                Skills_in_vacancies.objects.get_or_create(vacancy_id=vacancy, skill_name=tag, priority=2, obligation=1)
            for tag_name in matched_additionally_skills:
                tag, _ = SkillTag.objects.get_or_create(name=tag_name)
                Skills_in_vacancies.objects.get_or_create(vacancy_id=vacancy, skill_name=tag, priority=2, obligation=2)

        if matched_disciplines_skills or matched_additionally_skills:
            tagged_skills_count += 1

    vacancy_tag_coverage = (tagged_vacancies_count / total_vacancies) * 100
    skill_tag_coverage = (tagged_skills_count / total_vacancies) * 100

    print(f"Покрытие ролей: {vacancy_tag_coverage:.2f}%")
    print(f"Покрытие навыков: {skill_tag_coverage:.2f}%")

def check_vacancy_tags():
    onto_manager = OntologyManager.get_instance()
    if onto_manager.get_ontology() is None:
        last_loaded_file = FileUpload.objects.filter(tag_type='ontology', last_loaded=True).first()
        if last_loaded_file:
            onto_manager.load_ontology(last_loaded_file.file.path)
    ontology_skills_data = {}
    original_skills_data = {}

    for siv in Skills_in_vacancies.objects.all():
        skill_name = siv.skill_name.name.lower()
        vacancy_id = siv.vacancy_id_id
        original_skills_data.setdefault(vacancy_id, {}).update({skill_name: siv.obligation})

    for riv in Roles_in_vacancies.objects.all():
        role_name = riv.role_name.name
        vacancy_id = riv.vacancy_id_id
        role_instance = next((inst for inst in onto_manager.get_ontology().role.instances() if inst.name == role_name), None)
        if role_instance:
            ontology_skills_data.setdefault(vacancy_id, set()).update(get_skills_from_ontology(role_instance))
        else:
            if vacancy_id in original_skills_data:
                most_likely_role = infer_roles_from_skills(vacancy_id, original_skills_data[vacancy_id], onto_manager.get_ontology())
                if most_likely_role:
                    ontology_skills_data.setdefault(vacancy_id, set()).update(get_skills_from_ontology(most_likely_role))

    all_skills_data = {key: ontology_skills_data.get(key, set()).union(original_skills_data.get(key, set()))
                       for key in set(ontology_skills_data).union(set(original_skills_data))}

    update_vacancy_skills(all_skills_data, original_skills_data, ontology_skills_data)

def infer_roles_from_skills(vacancy_id, skills_dict, onto):
    possible_roles = {}
    skills_set = set(skills_dict.keys())

    ontology_classes = [onto.role, onto.field, onto.baserole]

    for role_class in ontology_classes:
        for instance in role_class.instances():
            role_skills = {skill.name.lower() for skill in instance.includes}
            if skills_set.intersection(role_skills):
                possible_roles[instance] = role_skills

    best_match = determine_best_match(possible_roles, skills_set)
    if best_match:
        print(f"Наилучшее соответствие для вакансии {vacancy_id} найдено: {best_match}.")
        update_role_in_vacancy(vacancy_id, best_match, role_priority=2)
        return best_match
    else:
        print(f"Ни одно соответствие для вакансии {vacancy_id} не найдено.")
        return None


def update_role_in_vacancy(vacancy_id, role_instance, role_priority=2):
    vacancy_tag, _ = VacancyTag.objects.get_or_create(name=role_instance.name)
    role_in_vacancy, created = Roles_in_vacancies.objects.update_or_create(
        vacancy_id_id=vacancy_id,
        role_name=vacancy_tag,
        defaults={'priority': role_priority}
    )
    if created:
        print(f"Создана новая роль для вакансии {vacancy_id} с приоритетом {role_priority}.")
    else:
        print(f"Роль для вакансии {vacancy_id} обновлена с приоритетом {role_priority}.")

def determine_best_match(possible_roles, skills):
    best_match = None
    max_intersection = 0
    for role, role_skills in possible_roles.items():
        intersection_size = len(skills.intersection(role_skills))
        if intersection_size > max_intersection:
            max_intersection = intersection_size
            best_match = role
    return best_match

def get_skills_from_ontology(role_instance):
    return {skill.name.lower() for skill in role_instance.includes}

def update_vacancy_skills(all_skills_data, original_skills_data, ontology_skills_data):
    with transaction.atomic():
        for vacancy_id, skills in all_skills_data.items():
            original_skills = original_skills_data.get(vacancy_id, {})
            ontology_skills = ontology_skills_data.get(vacancy_id, set())
            for skill_name in skills:
                if skill_name in original_skills:
                    obligation = original_skills[skill_name]
                else:
                    obligation = 2
                priority = determine_priority(skill_name, original_skills, ontology_skills)
                skill_tag, _ = SkillTag.objects.get_or_create(name=skill_name)
                Skills_in_vacancies.objects.update_or_create(
                    vacancy_id_id=vacancy_id,
                    skill_name=skill_tag,
                    obligation=obligation,
                    defaults={'priority': priority}
                )
                print(f"Навык '{skill_name}' для вакансии '{vacancy_id}' обновлен до приоритета {priority} с обязательностью {obligation}")

def determine_priority(skill_name, skill_details, ontology_skills):
    skill_in_original = skill_name in skill_details
    skill_in_ontology = skill_name in ontology_skills

    if skill_in_original and skill_in_ontology:
        obligation = skill_details[skill_name]
        return 1 if obligation == 1 else 2

    elif skill_in_original and not skill_in_ontology:
        obligation = skill_details[skill_name]
        return 3 if obligation == 1 else 4

    elif skill_in_ontology and not skill_in_original:
        return 5
