EMPTY_NAME = ""
PAGE = 1
EXPECTED_STATUS = 200
EXPECTED_BODY = {
    "total": 0,
    "items": []
}
LINK_TEXT = "Онлайн-кинотеатр"
EXPECTED_URL_PART = "https://hd.kinopoisk.ru/"  # часть URL, по которой проверим переход
LINK_TEXT = "Телеканалы"
EXPECTED_URL_PART = "https://hd.kinopoisk.ru/channels"
LINK_TEXT = "Фильмы"
EXPECTED_URL_PART = "https://www.kinopoisk.ru/lists/categories/movies/1/"
LINK_TEXT = "Сериалы"
EXPECTED_URL_PART = "https://www.kinopoisk.ru/lists/categories/movies/3/"
LINK_TEXT = "Спорт"
EXPECTED_URL_PART = "https://hd.kinopoisk.ru/sport/"
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
