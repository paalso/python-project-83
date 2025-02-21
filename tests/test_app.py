import pytest
from page_analyzer.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get('/')

    assert response.status_code == 200

    assert "Анализатор страниц" in response.text
    assert "Бесплатно проверяйте сайты на SEO-пригодность" in response.text

    assert '<input type="text" class="form-control" id="text" name="url"' in response.text
    assert 'placeholder="https://www.example.com"' in response.text
    assert 'Проверить' in response.text
    assert 'Url для проверки' in response.text

    assert 'href="/urls"' in response.text

    # Проверка наличия flash-сообщений
    # Если вы хотите протестировать наличие flash-сообщения, можете использовать флаг в тесте
    # Например, можно добавить flash-сообщение в тесте перед его вызовом
    # response = client.post('/urls', data={'url': 'invalid-url'})
    # assert b'Invalid URL' in response.data  # Пример текста flash-сообщения
