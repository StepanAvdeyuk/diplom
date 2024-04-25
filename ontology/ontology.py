from owlready2 import get_ontology


file_path = 'ontology/second.owx'
class OntologyManager:
    _instance = None
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.onto = get_ontology(f"file://{file_path}")
        self.onto.load()

    def get_ontology(self):
        return self.onto

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