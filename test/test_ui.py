import pytest
import requests
from selenium import webdriver
from main_page import MainPage
from env_config import BASE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LINK_TEXT = "Онлайн-кинотеатр"
EXPECTED_URL_PART = "https://hd.kinopoisk.ru/"
LINK_TEXT2 = "Телеканалы"
EXPECTED_URL_PART2 = "https://hd.kinopoisk.ru/channels"
LINK_TEXT3 = "Фильмы"
EXPECTED_URL_PART3 = "https://www.kinopoisk.ru/lists/categories/movies/1/"
LINK_TEXT4 = "Сериалы"
EXPECTED_URL_PART4 = "https://www.kinopoisk.ru/lists/categories/movies/3/"
LINK_TEXT5 = "Спорт"
EXPECTED_URL_PART5 = "https://hd.kinopoisk.ru/sport/"

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_online_cinema_navigation(driver):
    driver.get(BASE_URL)
    
    # Проверяем код ответа 200
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"Ожидался код 200, но получили {response.status_code}"
    
    main_page = MainPage(driver)
    main_page.click_kinopoisk_link(LINK_TEXT)
    
    # Проверка, что текущий URL содержит EXPECTED_URL_PART
    assert EXPECTED_URL_PART in driver.current_url, f"Ожидалось, что в URL будет '{EXPECTED_URL_PART}', но получили {driver.current_url}"

def test_tv_channels_link_navigation(driver):
    driver.get(BASE_URL)

    # Проверка кода ответа 200
    response = requests.get(driver.current_url)
    assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"

    main_page = MainPage(driver)
    main_page.click_kinopoisk_link(LINK_TEXT2)
    assert EXPECTED_URL_PART2 in driver.current_url, f"Ожидалось, что в URL будет '{EXPECTED_URL_PART2}', но получили {driver.current_url}"
  
    wait = WebDriverWait(driver, 10)

    # Проверка отображения списка Каналов 
    channels = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".styles_container__SqQJM")))
    assert len(channels) > 0, "Список каналов не отображается"

    # Проверка того, что фильмы видимы
    visible_channels = [m for m in channels if m.is_displayed()]
    assert len(visible_channels) > 0, "Каналы присутствуют, но не видимы"

def test_films_link_navigation(driver):
    driver.get(BASE_URL)

    # Проверка, что код ответа 200
    response = requests.get(driver.current_url)
    assert response.status_code == 200, f"Код ответа сервера не 200, а {response.status_code}" 

    main_page = MainPage(driver)
    main_page.click_kinopoisk_link(LINK_TEXT3)
    
    # Проверяем, что URL содержит ожидаемую часть
    assert EXPECTED_URL_PART3 in driver.current_url, f"Ожидалось, что в URL будет '{EXPECTED_URL_PART3}', но получили {driver.current_url}"

    # Проверяем, что список фильмов присутствует, предположим, что фильмы - элементы списка с классом "styles_meta__4NtO0"
    film_items = driver.find_element(By.CSS_SELECTOR, ".styles_meta__4NtO0")
 
    assert film_items is not None, "Список фильмов не найден"


def test_serial_navigation(driver):
    driver.get(BASE_URL)

    # Проверка, что код ответа 200 
    response = requests.get(driver.current_url)
    assert response.status_code == 200, f"Ожидался код 200, но получили {response.status_code}"

    main_page = MainPage(driver)
    main_page.click_kinopoisk_link(LINK_TEXT4)
    
    # Проверка, что в URL есть ожидаемая часть
    assert EXPECTED_URL_PART4 in driver.current_url, f"Ожидалось, что в URL будет '{EXPECTED_URL_PART4}', но получили {driver.current_url}"
    
    # Проверяем, что список сериалов присутствует, элементы списка с классом "styles_meta__4NtO0"
    serial_items = driver.find_element(By.CSS_SELECTOR, ".styles_meta__4NtO0")
    assert serial_items is not None, "Список сериалов не найден"

def test_sport_navigation(driver):
    driver.get(BASE_URL)

    # Проверка кода ответа 200
    response = requests.get(driver.current_url)
    assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"

    main_page = MainPage(driver)
    main_page.click_kinopoisk_link(LINK_TEXT5)
    assert EXPECTED_URL_PART5 in driver.current_url, f"Ожидалось, что в URL будет '{EXPECTED_URL_PART5}', но получили {driver.current_url}"
  
    wait = WebDriverWait(driver, 10)

    # Проверка отображения списка 
    sport = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".base-list_title-text__LuY5B")))
    assert len(sport) > 0, "Список спорт не отображается"

    # Проверка того спорт новости
    visible_sport = [m for m in sport if m.is_displayed()]
    assert len(visible_sport) > 0, "Спорт присутствует, но не видим"   