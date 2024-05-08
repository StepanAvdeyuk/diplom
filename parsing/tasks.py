from .parser import clear_data, get_data, upload_data
from ontology.scripts import tag_vacancies, check_vacancy_tags

def update_vacancies():
    print("Начинается обновление вакансий...")
    data = get_data()
    print("Данные получены")
    clear_data()
    print("Старые данные удалены")
    upload_data(data)
    print("Новые данные добавлены в базу данных")
    tag_vacancies()
    print("Обработка данных")
    check_vacancy_tags()
    print("Обновление вакансий завершено.")