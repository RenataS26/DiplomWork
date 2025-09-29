from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from env_config import TIMEOUT,BASE_URL, BASE_URL2, API_KEY, HEADERS, BASE_URL4,API_BASE_URL,API_PERSONS_ENDPOINT,BASE_URL3
import allure
import requests

class MainPage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открываем страницу {url}")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Проверяем статус код страницы")
    def check_status_code(self):
        response = requests.get(BASE_URL)
        assert response.status_code == 200, f"Ожидался код 200, но получили {response.status_code}"

    @allure.step("Кликаем по ссылке с текстом {link_text}")
    def click_kinopoisk_link(self, link_text):
        link = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.LINK_TEXT, link_text))
        )
        link.click()

    @allure.step("Проверяем, что URL содержит '{expected_part}'")
    def url_contains(self, expected_part: str) -> bool:
        return expected_part in self.driver.current_url

    @allure.step("Ожидаем видимость списка каналов")
    def wait_for_channels_list_visible(self):
        channels = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".styles_container__SqQJM"))
        )
        if not channels:
            raise AssertionError("Список каналов не отображается")

        visible_channels = [m for m in channels if m.is_displayed()]
        if not visible_channels:
            raise AssertionError("Каналы присутствуют, но не видимы")

        return visible_channels

    @allure.step("Проверяем присутствие списка фильмов")
    def is_film_list_present(self) -> bool:
        films = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".styles_meta__4NtO0"))
        )
        if not films:
            raise AssertionError("Список не отображается")

        visible_films = [m for m in films if m.is_displayed()]
        if not visible_films:
            raise AssertionError("Список присутствует, но не видим")

        return visible_films

    @allure.step("Проверяем присутствие списка спортивных передач")
    def is_sport_list_present(self) -> bool:
        sports = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".base-list_title-text__LuY5B"))
        )
        if not sports:
            raise AssertionError("Список не отображается")

        visible_sports = [m for m in sports if m.is_displayed()]
        if not visible_sports:
            raise AssertionError("Список присутствует, но не видим")

        return visible_sports
    
    
class FilmApi:
    def __init__(self):
        self.base_url = BASE_URL2
        self.headers = {
            "X-API-KEY": API_KEY,
            "Accept": "application/json"
        }

    @allure.step("Получение информации о фильме по ID: {film_id}")
    def get_film_by_id(self, film_id):
        url = f"{self.base_url}/{film_id}"
        response = requests.get(url, headers=self.headers, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

class PersonAPI:
    def __init__(self):
        self.url = API_BASE_URL + API_PERSONS_ENDPOINT
        self.headers = {
            "Accept": "application/json",
            "X-API-KEY": API_KEY  
        }

    @allure.step("Поиск персонажей по имени: '{name}', страница: {page}")
    def get_persons_by_name(self, name, page=1):
        params = {
            "name": name,
            "page": page
        }
        response = requests.get(self.url, headers=self.headers, params=params)
        return response

class FilmsSearchPage:

    def __init__(self, keyword, page):
        self.keyword = keyword
        self.page = page

    def search_film(self):
        params = {
            "keyword": self.keyword,
            "page": self.page
        }
        response = requests.get(BASE_URL4, headers=HEADERS, params=params)
        return response

class FilmsPage:
    def __init__(self, film_id):
        self.url = BASE_URL3 + str(film_id)

    @allure.step("Отправка PUT запроса для фильма с именем '{film_name}'")
    def put_film(self, film_name):
        payload = {
            "name": film_name
        }
        response = requests.put(self.url, headers=HEADERS, json=payload)
        return response

class SearchPage:
    def __init__(self, keyword, page=1):
        self.keyword = keyword
        self.page = page

    def search_films(self):
        params = {
            "keyword": self.keyword,
            "page": self.page
        }
        response = requests.get(BASE_URL4, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json() 

     






