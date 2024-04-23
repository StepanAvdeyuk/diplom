from owlready2 import get_ontology

# Путь к файлу OWX
file_path = 'ontology/second.owx'

# Загрузка онтологии из файла
ontology = get_ontology(f"file://{file_path}").load()

# Вывести список всех классов в онтологии
for cls in ontology.classes():
    print(f"Класс: {cls}")
    print("Свойства:")
    for prop in cls.get_class_properties():  # Использование get_class_properties вместо get_properties
        for range_cls in prop.range:
            print(f"  {prop.name} диапазон: {range_cls}")

    print("Индивиды:")
    for instance in cls.instances():
        print(f"  {instance}")
    print("\n")

# # Перебор всех свойств и анализ связей между классами
# for prop in ontology.properties():
#     print(f"Свойство: {prop.name}")
#     for domain in prop.domain:
#         for range in prop.range:
#             print(f"  От {domain} до {range}")

# for field in ontology.role.instances():
#     print(f"Связи для индивида {field.name}:")
#     for prop in field.get_properties():
#         for value in prop[field]:
#             print(f"  {prop.python_name} -> {value}")
#     print("\n")


# Функция для поиска всех Role, которые включают данный Skill
# def find_roles_by_skill(skill_name):
#     skill = ontology.search_one(iri="*"+skill_name)  # Поиск skill по имени
#     if skill:
#         roles = [role for role in ontology.role.instances() if skill in role.includes]
#         return roles
#     else:
#         return []
#
# # Пример использования функции
# skill_name = "css"  # Замените на имя интересующего вас Skill
# roles_including_skill = find_roles_by_skill(skill_name)
# for role in roles_including_skill:
#     print(f"Role {role.name} includes Skill {skill_name}")