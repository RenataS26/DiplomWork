from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from env_config import TIMEOUT, BASE_URL2, API_KEY, HEADERS, BASE_URL4,API_BASE_URL,API_PERSONS_ENDPOINT,BASE_URL3
import allure
import requests
import testdata


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Клик по ссылке с текстом '{link_text}'")
    def click_kinopoisk_link(self, link_text):
        link_locator = (By.LINK_TEXT, link_text)
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(link_locator)
        ).click()

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

     






