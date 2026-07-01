"""
Тот же самый парсинг одной страницы books.toscrape.com, но через XPath
вместо CSS-селекторов — чтобы показать оба подхода на практике.

CSS-селектор из parser.py       →  Эквивалентный XPath здесь
"article.product_pod"            →  //article[@class="product_pod"]
"h3 a" (атрибут title)           →  .//h3/a/@title
"p.price_color"                  →  .//p[@class="price_color"]/text()
"p.instock.availability"         →  .//p[contains(@class, "instock")]
"""

import requests
from lxml import html

URL = "https://books.toscrape.com/"


def scrape_page_with_xpath(url):
    headers = {"User-Agent": "Mozilla/5.0 (educational scraping practice)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    # lxml.html.fromstring строит дерево документа, по которому можно
    # ходить XPath-выражениями — так же, как select() ходит по CSS-селекторам
    tree = html.fromstring(response.text)

    books = []
    # xpath() возвращает список узлов, подходящих под выражение
    cards = tree.xpath('//article[@class="product_pod"]')

    for card in cards:
        # ./  в начале — значит "искать внутри текущей карточки", а не по всей странице
        title = card.xpath('.//h3/a/@title')[0]

        price_raw = card.xpath('.//p[@class="price_color"]/text()')[0]
        price = float(price_raw.replace("£", "").replace("Â", ""))

        availability = card.xpath(
            './/p[contains(@class, "instock")]/text()'
        )[1].strip()  # [0] — перенос строки, [1] — сам текст "In stock"

        books.append({"title": title, "price_gbp": price, "availability": availability})

    return books


if __name__ == "__main__":
    books = scrape_page_with_xpath(URL)
    print(f"Собрано книг с первой страницы через XPath: {len(books)}")
    for b in books[:5]:
        print(b)
