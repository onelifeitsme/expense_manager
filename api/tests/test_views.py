from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from transaction.models import TransactionCategory
from api.serializers import TransactionCategorySerializer, StatisticsCategorySerializer


def test_retrieve_user_balance(jwt_token_access):
    """Тест просотра баланса авторизованным пользователем"""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token_access)
    response = client.get(path=reverse('account_detail'))
    assert 'balance' in response.data

def test_retrieve_default_categories(jwt_token_access):
    """Тест проверки наличия стандартных категорий у пользователя"""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token_access)
    response = client.get(path=reverse('categories_list'))
    serializer = TransactionCategorySerializer(data=response.data, many=True)
    serializer.is_valid()
    retrieved_categories = [category['name'] for category in serializer.validated_data]
    assert retrieved_categories == list(TransactionCategory.DEFAULT_CATEGORIES)

def test_create_category(jwt_token_access):
    """Тест создания категории"""
    data = {
        'name': 'Новая категория',
    }
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token_access)
    response = client.post(path=reverse('categories_list'), data=data)
    assert response.status_code == 201

def test_create_transaction(new_user, jwt_token_access):
    """Тест создания транзакции"""
    data = {
        'amount': '900',
        'category': new_user.categories.first().pk,
        'organization' : 'organization',
        'description': 'description',
    }
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token_access)
    response = client.post(path=reverse('transactions_list'), data=data)
    assert response.status_code == 201

def test_retrieve_statistics(new_user, few_transactions, jwt_token_access):
    """Тест получения статистики"""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token_access)
    response = client.get(path=reverse('account_statistics'))
    serializer = StatisticsCategorySerializer(data=response.data, many=True)
    serializer.is_valid()
    assert sum([item['result'] for item in serializer.validated_data[:3]]) == 300


