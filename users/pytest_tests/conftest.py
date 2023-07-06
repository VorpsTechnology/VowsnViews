from users.models import User

import pytest


@pytest.fixture()
def user_data():
    return {
            'user_full_name': 'pytest_tests',
            'email': 'pytest_tests@gmail.com',
            'password': 'Test@321',
            'phone_number': 1234567890,
            'is_active': True
            }


@pytest.fixture()
def create_test_user(user_data):
    test_user = User.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    return test_user


@pytest.fixture()
def authenticated_user(client, user_data):
    test_user = User.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    test_user.save()
    client.login(**user_data)
    return test_user

