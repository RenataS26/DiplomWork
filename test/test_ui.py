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
    page = MainPage(driver)

    page.open(BASE_URL)
    page.check_status_code()
    page.click_kinopoisk_link(LINK_TEXT)

    assert page.url_contains(EXPECTED_URL_PART), \
        f"Ожидалось, что в URL будет '{EXPECTED_URL_PART}', но получили {driver.current_url}"


def test_tv_channels_link_navigation(driver):
    page = MainPage(driver)
    page.open(BASE_URL)
    
    page.click_kinopoisk_link(LINK_TEXT2)
    assert page.url_contains(EXPECTED_URL_PART2), \
        f"Ожидалось, что в URL будет '{EXPECTED_URL_PART2}', но получили {driver.current_url}"

    page.wait_for_channels_list_visible()


def test_films_link_navigation(driver):
    page = MainPage(driver)
    page.open(BASE_URL)

    page.click_kinopoisk_link(LINK_TEXT3)

    assert page.url_contains(EXPECTED_URL_PART3), \
        f"Ожидалось, что в URL будет '{EXPECTED_URL_PART3}', но получили {driver.current_url}"

    assert page.is_film_list_present(), "Список фильмов не найден"


def test_serial_navigation(driver):
    page = MainPage(driver)
    page.open(BASE_URL)

    page.click_kinopoisk_link(LINK_TEXT4)

    assert page.url_contains(EXPECTED_URL_PART4), \
        f"Ожидалось, что в URL будет '{EXPECTED_URL_PART4}', но получили {driver.current_url}"

    assert page.is_film_list_present(), "Список не найден"


def test_sport_navigation(driver):
    page = MainPage(driver)
    page.open(BASE_URL)

    page.click_kinopoisk_link(LINK_TEXT5)

    assert page.url_contains(EXPECTED_URL_PART5), \
        f"Ожидалось, что в URL будет '{EXPECTED_URL_PART5}', но получили {driver.current_url}"

    assert page.is_sport_list_present(), "Список не найден"  