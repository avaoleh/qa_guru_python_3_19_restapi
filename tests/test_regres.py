import requests
from requests import Response
from pytest_voluptuous import S
from schemas import schemas
from mimesis.enums import Locale, Gender
from mimesis import Person


def test_create_user(regres):
    # GIVEN:
    person = Person(Locale.EN)
    user_data = {
        'name': person.first_name(gender=Gender.MALE),
        'job': person.occupation(),
    }

    # WHEN:
    response: Response = regres.post(
        url='/api/users',
        data=user_data
    )

    # THEN:
    assert response.status_code == 201
    assert response.json() == S(schemas.create_user)
    # logging.info(response.json())
    assert response.json()['name'] == user_data['name']
    assert response.json()['job'] == user_data['job']


def test_update_user(regres):
    # GIVEN:
    person = Person(Locale.EN)
    updated_user_data = {
        'name': person.first_name(gender=Gender.MALE),
        'job': person.occupation(),
    }

    # WHEN:
    response: Response = regres.put(
        url='/api/users/2',
        data=updated_user_data
    )

    # THEN:
    assert response.status_code == 200
    assert response.json() == S(schemas.update_user)
    assert response.json()['name'] == updated_user_data['name']
    assert response.json()['job'] == updated_user_data['job']


def test_delete_user(regres):
    # WHEN:
    response: Response = regres.delete(
        url='/api/users/2',
    )

    # THEN:
    assert response.status_code == 204


def test_register_user_successful(regres):
    # GIVEN:
    register_user_data = {
        'email': 'eve.holt@reqres.in',
        'password': 'pistol',
    }

    # WHEN:
    user_register: Response = regres.post(
        url='/register',
        data=register_user_data
    )

    # THEN:
    assert user_register.status_code == 200
    assert user_register.json() == S(schemas.register_user)
    assert user_register.json()['id']
    assert user_register.json()['token']


def test_register_user_unsuccessful(regres):
    # GIVEN:
    register_user_data_unsuccessful = {
        "email": "eve.holt@reqres.in",
    }

    # WHEN:
    user_register: Response = regres.post(
        url='/register',
        data=register_user_data_unsuccessful
    )

    # THEN:
    assert user_register.status_code == 400
    assert user_register.json()['error'] == 'Missing password'


def test_login_user_successful(regres):
    # GIVEN:
    login_user_data = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    # WHEN:
    login_user: Response = regres.post(
        url='/login',
        data=login_user_data
    )

    # THEN:
    assert login_user.status_code == 200
    assert login_user.json() == S(schemas.login_user)
    assert login_user.json()["token"] is not None


def test_login_user_unsuccessful(regres):
    # GIVEN:
    login_user_data_unsuccessful = {
        "email": "eve.holt@reqres.in"
    }

    # WHEN:
    login_user: Response = regres.post(
        url='/login',
        data=login_user_data_unsuccessful
    )

    # THEN:
    assert login_user.status_code == 400
    assert login_user.json()['error'] == 'Missing password'
    assert len(login_user.content) != 0
