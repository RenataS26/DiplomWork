import pytest
import allure
from selenium import webdriver
from main_page import MainPage
from env_config import BASE_URL
import testdata

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()  
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.step("Открыть главную страницу {url}")
def open_main_page(driver, url):
    driver.get(url)

@allure.step("Кликнуть по ссылке с текстом '{link_text}'")
def click_link(main_page, link_text):
    main_page.click_kinopoisk_link(link_text)

@allure.step("Проверить, что текущий URL содержит '{expected_part}'")
def check_url_contains(driver, expected_part):
    assert expected_part in driver.current_url, \
        f"Ожидалось, что в URL будет '{expected_part}', но получили {driver.current_url}"

@pytest.mark.parametrize("test_name", [
    "online_cinema_navigation",
    "tv_channels_link_navigation",
    "films_link_navigation",
    "serial_navigation",
    "sport_navigation"
])
def test_navigation(driver, test_name):
    """
    Универсальный тест навигации с шагами allure.
    Можно расширять под разные сценарии, если понадобится.
    """
    with allure.step(f"Запуск теста {test_name}"):
        open_main_page(driver, BASE_URL)
        main_page = MainPage(driver)
        click_link(main_page, testdata.LINK_TEXT)
        check_url_contains(driver, testdata.EXPECTED_URL_PART)
    