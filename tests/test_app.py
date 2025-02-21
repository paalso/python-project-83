import pytest
from page_analyzer.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_homepage_content_and_url_validation(client):
    """Checks home page content and URL validation"""

    response = client.get('/')
    assert response.status_code == 200

    assert "Анализатор страниц" in response.text
    assert "Бесплатно проверяйте сайты на SEO-пригодность" in response.text
    assert '<input type="text" class="form-control" id="text" name="url"' in response.text
    assert 'placeholder="https://www.example.com"' in response.text
    assert 'Проверить' in response.text
    assert 'Url для проверки' in response.text
    assert 'href="/urls"' in response.text

    incorrect_url_answer = 'Некорректный URL'
    extremely_long_url_answer = 'URL превышает 255 символов'
    valid_url = 'https://www.example.com'
    extremely_long_url = 'https://www.' + 'a' * 240 + '.net'

    response = client.post('/urls', data={'url': 'invalid-url'})
    assert incorrect_url_answer in response.text
    assert extremely_long_url_answer not in response.text

    response = client.post('/urls', data={'url': extremely_long_url})
    assert extremely_long_url_answer in response.text
    assert incorrect_url_answer not in response.text

    response = client.post('/urls', data={'url': valid_url})
    assert response.status_code == 200
    assert incorrect_url_answer not in response.text
    assert extremely_long_url_answer not in response.text
