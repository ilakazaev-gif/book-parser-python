"""
Парсер каталога books.toscrape.com — учебного сайта-магазина книг,
специально созданного для тренировки скрапинга (легально, без ToS-проблем).

Что делает скрипт:
1. Проходит по всем страницам каталога (пагинация)
2. С каждой страницы вытаскивает: название книги, цену, наличие, рейтинг
3. Сохраняет результат в books.csv и books.json
"""

import csv
import json
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/"

# На сайте рейтинг закодирован словом внутри CSS-класса: "star-rating Three".
# Простого числа в HTML нет — приходится сопоставлять словами вручную.
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_soup(url):
    """Скачивает страницу по url и возвращает объект BeautifulSoup для парсинга."""
    # User-Agent говорит серверу, что запрос идёт "как из браузера" —
    # без него некоторые сайты отдают другой ответ или блокируют запрос.
    headers = {"User-Agent": "Mozilla/5.0 (educational scraping practice)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # если сервер вернул ошибку (404, 500) — сразу упадём с исключением
    return BeautifulSoup(response.text, "html.parser")


def parse_book_card(card):
    """Достаёт название, цену, наличие и рейтинг из одной карточки книги (<article class="product_pod">)."""
    # card.select_one(...) — берёт ПЕРВЫЙ элемент по CSS-селектору внутри карточки
    title = card.select_one("h3 a")["title"]

    price_text = card.select_one("p.price_color").text  # например "£51.77"
    price = float(price_text.replace("£", "").replace("Â", ""))  # превращаем строку в число

    availability = card.select_one("p.instock.availability").text.strip()

    # У тега <p class="star-rating Three"> нужное слово — второй CSS-класс.
    rating_class = card.select_one("p.star-rating")["class"]  # ['star-rating', 'Three']
    rating_word = rating_class[1]
    rating = RATING_WORDS.get(rating_word, 0)

    return {
        "title": title,
        "price_gbp": price,
        "availability": availability,
        "rating": rating,
    }


def scrape_all_books():
    """Проходит по всем страницам каталога и собирает данные по каждой книге."""
    books = []
    page_num = 1
    url = START_URL

    while True:
        print(f"Парсим страницу {page_num}: {url}")
        soup = get_soup(url)

        cards = soup.select("article.product_pod")
        for card in cards:
            books.append(parse_book_card(card))

        # Ищем ссылку "next" — если её нет, значит это последняя страница каталога
        next_link = soup.select_one("li.next a")
        if not next_link:
            break

        page_num += 1
        # urljoin правильно собирает абсолютный URL из текущего адреса и относительной
        # ссылки — сама разбирается, где страница лежит (в корне или в подпапке catalogue/)
        url = urljoin(url, next_link["href"])

        time.sleep(0.5)  # вежливая пауза между запросами, чтобы не долбить сервер слишком часто

    return books


def save_to_csv(books, filename="books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price_gbp", "availability", "rating"])
        writer.writeheader()
        writer.writerows(books)


def save_to_json(books, filename="books.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    all_books = scrape_all_books()
    save_to_csv(all_books)
    save_to_json(all_books)
    print(f"\nГотово! Собрано книг: {len(all_books)}")
    print("Сохранено в books.csv и books.json")
