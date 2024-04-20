import requests
import json
from parsing.models import Heads, Types, Stage, Projects, Vacancies

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'x-auth-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MDU3NzE2MjIsImV4cCI6MTcyMzA1MTYyMiwidXNlcm5hbWUiOiLQmtGD0LvRjNC60L4g0JzQsNC60YHQuNC8INCQ0LvQtdC60YHQtdC10LLQuNGHIiwiZW1haWwiOiJtYWt1bGtvQGVkdS5oc2UucnUiLCJzdGFmZiI6ZmFsc2UsInN0dWRlbnQiOnRydWV9.S0RuXgcKlDl1CbBVbkiCAIS-EOZugn8S0cWyEGPJMD-ZuPHQXJ0uVHdsT4VE6SezmM2N9esEFg2-Y8ayRDYX35c0fRQE8UYwGmsbJ_kb25Bz8X5OuEXYNKIoVauEG3vmuvsaPimUP7-K1bily6u5nJ6jSWICE9L11LGK1dkItOdr896k5yGSwD7DXnIXoNsM7miaAMwH84fvjQ16OzQsoD8X3_kOCHcxwq71EtfrPMojgUas5bGwYMvYO0H-sX-88_CAS7U6gJXQSZidRuQzeNaEbMwDStVvYKHYrKtJe999j2PbMWqRLbKm62hbAUKfTRddSZGT13iXA3mQg-aaSUimII_duOzicch4Qd3ee0HhzeulfJcjNAJfahyyQWY1JiDvFy_Gt2P8rGVPJJ6WbGFqPZtU39uan0pl_m6u6lyd728xMa4JxK3UVkQyxvG7prOsUL2bNC2JdAhrgbmCGT93GUk1q7lQUexoHAEWT-T3dg2WIsQqiG8NVrvpJQfx4otnwPcrI-wl1AR3QttFZ2VX_1iYC_gveq8VoEvM7T3Jn6Gq8l6JnH2WYD-koSIqOSjsW3zEAB12PYIN8rmYZiNwavn6gjen1eEuaBTS9YZIZedB_62MvcX_epoaw2R25dI-dro3kQGaXA9mfLXBL6O-cJyMDvwSBfM8Xpr5dvQ',
}

response = requests.get(
    'https://cabinet.miem.hse.ru/api/projects?limit=500&statusIds[]=1&statusIds[]=2', headers=headers, )

projects_data = response.json()

selected_projects = []


def get_data():
    for project in projects_data['data']['projects']:
        if project['vacancies'] != 0:
            selected_project_info = {
                'id': project['id'],
                'name': project['nameRus'],
                'type': project['type'],
                'head': project['head'],
                'url': f"https://cabinet.miem.hse.ru/#/project/{project['id']}/"
            }
            selected_projects.append(selected_project_info)

    # Цикл по всем проектам в selected_items
    for project in selected_projects:
        project_url = f"https://cabinet.miem.hse.ru/api/project/vacancies/{project['id']}"
        project_header_url = f"https://cabinet.miem.hse.ru/api/project/header/{project['id']}"

        response1 = requests.get(project_url, headers=headers)
        response2 = requests.get(project_header_url, headers=headers)
        vacancies_data = response1.json()
        headers_data = response2.json()

        vacancies = []

        for vacancy in vacancies_data['data']:
            if vacancy['booked'] == False:
                vacancy_info = {
                    'vacancy_id': vacancy['vacancyId'],
                    'role': vacancy['role'],
                    'count': vacancy['count'],
                    'disciplines': vacancy['disciplines'],
                    'additionally': vacancy['additionally']
                }
                vacancies.append(vacancy_info)

        for head in headers_data['data']['mainLeader']:
            head_email = head['email']

        stages = []
        for stage in headers_data['data']['timeline']:
            stage_info = {
                'stage_id': stage['id'],
                'stage_name': stage['name'],
                'status': stage['status'],
                'date': stage['date'],
                'sessionStartDate': stage['sessionStartDate'],
                'sessionEndDate': stage['sessionEndDate']
            }
            stages.append(stage_info)

        project['stages'] = stages
        project['vacancies'] = vacancies
        project['head_email'] = head_email

    return selected_projects


def clear_data():
    Heads.objects.all().delete()
    Types.objects.all().delete()
    Projects.objects.all().delete()
    Stage.objects.all().delete()
    Vacancies.objects.all().delete()


def upload_data():
    for project in selected_projects:
        name_parts = project['head'].split()

        head_surname = name_parts[0] if len(name_parts) > 0 else None
        head_name = name_parts[1] if len(name_parts) > 1 else None
        head_fathername = name_parts[2] if len(name_parts) > 2 else None

        heads_info = Heads(head_email=project['head_email'], head_name=head_name,
                           head_surname=head_surname, head_fathername=head_fathername)
        heads_info.save()

        types_info = Types(type_name=project['type'])
        types_info.save()

        project_head = Heads.objects.get(head_email=project['head_email'])
        projects_info = Projects(project_id=project['id'], project_name=project['name'],
                                 project_head=project_head, project_type=types_info,
                                 project_url=project['url'])
        projects_info.save()

        for vacancy in project['vacancies']:
            vacancy_project = Projects.objects.get(project_id=project['id'])
            vacancies_info = Vacancies(vacancy_id=vacancy['vacancy_id'], vacancy_name=vacancy['role'].strip(),
                                       vacancy_project=vacancy_project, vacancy_disciplines=vacancy['disciplines'],
                                       vacancy_additionally=vacancy['additionally'], vacancy_count=vacancy['count'])
            vacancies_info.save()

        for stage in project['stages']:
            stage_project = Projects.objects.get(project_id=project['id'])
            stages_info = Stage(stage_id=stage['stage_id'], stage_project=stage_project,
                                 stage_name=stage['stage_name'], stage_status=stage['status'], date=stage['date'],
                                 sessionStartDate=stage['sessionStartDate'], sessionEndDate=stage['sessionEndDate'])
            stages_info.save()
