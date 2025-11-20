import pytest

import main

TEST_DATA_TXT_1 = '''name,position,completed_tasks,performance,skills,team,experience_years
David Chen,Mobile Developer,36,4.6,"Swift, Kotlin, React Native, iOS",Mobile Team,3
Elena Popova,Backend Developer,43,4.8,"Java, Spring Boot, MySQL, Redis",API Team,4
Chris Wilson,DevOps Engineer,39,4.7,"Docker, Jenkins, GitLab CI, AWS",Infrastructure Team,5
Olga Kuznetsova,Frontend Developer,42,4.6,"Vue.js, JavaScript, Webpack, Sass",Web Team,3
Robert Kim,Data Engineer,34,4.7,"Python, Apache Spark, Airflow, Kafka",Data Team,4
Julia Martin,QA Engineer,38,4.5,"Playwright, Jest, API Testing",Testing Team,3
Tom Anderson,Backend Developer,49,4.9,"Go, Microservices, gRPC, PostgreSQL",API Team,7
Lisa Wang,Mobile Developer,33,4.6,"Flutter, Dart, Android, Firebase",Mobile Team,2
Mark Thompson,Data Scientist,31,4.7,"R, Python, TensorFlow, SQL",AI Team,4'''

TEST_DATA_TXT_2 = '''name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,"Python, Django, PostgreSQL, Docker",API Team,5
Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript, Redux, CSS",Web Team,4
John Smith,Data Scientist,29,4.6,"Python, ML, SQL, Pandas",AI Team,3
Anna Lee,DevOps Engineer,52,4.9,"AWS, Kubernetes, Terraform, Ansible",Infrastructure Team,6
Mike Brown,QA Engineer,41,4.5,"Selenium, Jest, Cypress, Postman",Testing Team,4
Sarah Johnson,Fullstack Developer,47,4.7,"JavaScript, Node.js, React, MongoDB",Web Team,5'''

TEST_DATA_TXT_3 = '''{
    "name": "David Chen",
    "position": "Mobile Developer",
    "completed_tasks": 36,
    "performance": 4.6,
    "skills": "Swift, Kotlin, React Native, iOS",
    "team": "Mobile Team",
    "experience_years": 3
}'''


@pytest.fixture(scope='session')
def session_temp_dir(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp('data')

    (temp_dir / 'test_data_1.csv').write_text(TEST_DATA_TXT_1)
    (temp_dir / 'test_data_2.csv').write_text(TEST_DATA_TXT_2)
    (temp_dir / 'test_data_3.json').write_text(TEST_DATA_TXT_3)

    return temp_dir


@pytest.fixture(scope='session')
def csv_file_paths(session_temp_dir):
    return [str(session_temp_dir / 'test_data_1.csv'), str(session_temp_dir / 'test_data_2.csv')]


@pytest.fixture(scope='session')
def json_file_path(session_temp_dir):
    return str(session_temp_dir / 'test_data_3.json')


@pytest.fixture(scope='session')
def session_parser():
    return main.create_parser()
