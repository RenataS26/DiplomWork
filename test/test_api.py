import pytest
from main_page import  FilmApi,FilmsSearchPage, FilmsPage,SearchPage,PersonAPI
import allure

EMPTY_NAME = ""
PAGE = 1
EXPECTED_STATUS = 200
EXPECTED_BODY = {
    "total": 0,
    "items": []
}
FILM_ID = 2213
EXPECTED_FILM_NAME = "Титаник"
PAGE = 1
TEST_DATA = {
    "keyword": "1984",
    "page": 1
}
TEST_DATA2 = {
    "film_id": 2213,
    "invalid_method_film_name": "Титаник"
}
SEARCH_KEYWORD = "&&&&"


class TestFilmApi:
    
 @allure.step("Отправка запроса на получение фильма по ID")
 def test_get_film_titanic(self):
    api = FilmApi()
    response = api.get_film_by_id(FILM_ID)

    with allure.step("Проверка наличия названия фильма на русском"):
        assert "nameRu" in response, "В ответе отсутствует название фильма на русском"
        
    with allure.step(f"Проверка соответствия названия '{EXPECTED_FILM_NAME}'"):
        assert EXPECTED_FILM_NAME.lower() in response["nameRu"].lower(), \
            f"Ожидаемое название '{EXPECTED_FILM_NAME}' не совпадает с '{response['nameRu']}'"


@pytest.fixture
def api():
    return PersonAPI()

@allure.step("Поиск актера по пустому имени")
def test_search_actor_by_empty_name(api):
    with allure.step(f"Отправка запроса поиска актера с пустым именем '{EMPTY_NAME}' и страницей {PAGE}"):
        response = api.get_persons_by_name(EMPTY_NAME, PAGE)
        
    with allure.step(f"Проверка статус-кода {EXPECTED_STATUS}"):
        assert response.status_code == EXPECTED_STATUS, f"Ожидался статус {EXPECTED_STATUS}, но получен {response.status_code}"
    
    json_body = response.json()
    
    with allure.step("Проверка тела ответа"):
        assert json_body == EXPECTED_BODY, f"Ожидалось тело {EXPECTED_BODY}, но получено {json_body}"


@allure.step("Поиск цифры")
def test_search_by_keyword():
    films_page = FilmsSearchPage(TEST_DATA['keyword'], TEST_DATA['page'])

    with allure.step(f"Отправка запроса поиска фильма с ключевым словом '{TEST_DATA['keyword']}'"):
        response = films_page.search_film()

    with allure.step("Проверка статус-кода 200"):
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    data = response.json()

    with allure.step("Проверка наличия поля 'films' в ответе"):
        assert 'films' in data, "Response JSON does not contain 'films' field"

    with allure.step("Проверка, что список фильмов не пустой"):
        assert len(data['films']) > 0, "Films list is empty"

    with allure.step("Проверка наличия ключевого слова '1984' в названиях фильмов"):
        found = any("1984" in (film.get('nameRu', '') + film.get('nameEn', '')) for film in data['films'])
        assert found, "Keyword '1984' not found in any film titles in response"


@allure.step("Негативный тест запроса PUT к фильму")
def test_put_film_method_not_allowed():
    film_page = FilmsPage(TEST_DATA2["film_id"])

    with allure.step(f"Отправка запроса PUT с именем '{TEST_DATA2['invalid_method_film_name']}'"):
        response = film_page.put_film(TEST_DATA2["invalid_method_film_name"])

    with allure.step("Проверка кода ответа 500"):
        assert response.status_code == 500, f"Expected 405 Method Not Allowed, got {response.status_code}"
        print("Негативный тест пройден: PUT на endpoint для фильма с кириллицей вернул 500")


@allure.step("Поиск фильмов с использованием специальных символов '&&&'")
def test_search_films_with_special_chars():
    search_page = SearchPage(keyword=SEARCH_KEYWORD, page=PAGE)
    
    with allure.step(f"Поиск фильмов по ключевому слову '{SEARCH_KEYWORD}'"):
        result = search_page.search_films()
    
    films = result.get("films", [])
    
    with allure.step("Проверка, что возвращается список фильмов"):
        assert isinstance(films, list), "Ожидается список фильмов"
    
    with allure.step("Проверка, что список фильмов не пустой"):
        assert len(films) > 0, "Список фильмов не должен быть пустым при поиске '&&&&'"

