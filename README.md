# Парсер каталога books.toscrape.com

Учебный проект: парсер на Python, который проходит по всем страницам
книжного каталога [books.toscrape.com](https://books.toscrape.com/) —
сайта, специально созданного для тренировки скрапинга — и собирает
данные по каждой книге: название, цену, наличие, рейтинг.

## Что демонстрирует проект

- Запросы к сайту через `requests` с заголовком `User-Agent`
- Парсинг HTML через `BeautifulSoup` и CSS-селекторы
- Обход пагинации с корректной сборкой относительных ссылок (`urljoin`)
- Экспорт результата в CSV и JSON
- Вежливая задержка между запросами (`time.sleep`), чтобы не перегружать сервер

## Как запустить

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python parser.py
```

На выходе — `books.csv` и `books.json` с данными по всем ~1000 книгам каталога.

## Результат

Собрано книг: 1000. Пример строки из `books.csv`:

```
title,price_gbp,availability,rating
A Light in the Attic,51.77,In stock,3
```
