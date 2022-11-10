import pytest
from account.models import User
from transaction.models import Transaction
from rest_framework.reverse import reverse


@pytest.fixture
def new_user(db) -> User:
    """Фикстура создания юзера"""
    return User.objects.create_user(email='testemail@gmail.com', password='testpassword')

@pytest.fixture
def jwt_token_access(new_user, client):
    """Фикстура получения токена"""
    data = {
        "email": new_user.email,
        "password": 'testpassword'
    }
    response = client.post(path=reverse('jwt-create'), data=data)
    return response.data.get('access')

@pytest.fixture
def few_transactions(new_user, db):
    """Фикстура создания нескольких транзакций"""
    for category in new_user.categories.all()[:3]:
        Transaction.objects.create(
            user=new_user,
            amount=100,
            category=category,
            organization='organization',
            description='description',
        )