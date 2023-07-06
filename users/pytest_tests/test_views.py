from django import urls

from users.models import User
import pytest


@pytest.mark.parametrize('param', [
    'users-login',
    'users-register',
    'home-dashboard',
    'users-logout',
    # 'users-checklist',
    # 'users-guest-list',
    # 'users-budget-list',
    # 'users-address-list',
    # 'dashboard',
    # 'users-address-add',
])
@pytest.mark.django_db
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    response = client.get(temp_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_login(client, user_data, create_test_user):
    assert User.objects.count() == 1
    login_url = urls.reverse('users-login')
    response = client.post(login_url, data=user_data)
    assert response.status_code == 302
    assert response.url == urls.reverse('home')


@pytest.mark.django_db
def test_user_logout(client, authenticated_user):
    assert User.objects.count() == 1
    logout_url = urls.reverse('users-logout')
    response = client.post(logout_url)
    assert response.status_code == 200
