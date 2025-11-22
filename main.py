# main.py
"""
Собирает товары:
  1) Книги с https://books.toscrape.com/
  2) Ноутбуки с https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops

Сохраняет всё в data/prices.csv и печатает простую аналитику.

Пример:
    # Собрать 2 страницы книг + ноутбуки, показать аналитику
    python main.py
    
    # Собрать 5 страниц книг
    python main.py --max-book-pages 5

    # Только собрать данные, без анализа
    python main.py --no-analyze
"""

import argparse

from fetcher import fetch_page
from parsers import parse_books_page, parse_laptops_page
from storage import save_products_to_csv
from analysis import print_basic_stats


BOOKS_BASE_URL = "https://books.toscrape.com/"
LAPTOPS_URL = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
DEFAULT_OUTPUT = "data/prices.csv"


def scrape_books(max_pages: int):
    """
    Скрапит книги с Books to Scrape, проходя по пагинации.
    """
    url = BOOKS_BASE_URL
    all_products = []
    page_num = 0

    while url and page_num < max_pages:
        page_num += 1
        print(f"[Books] Страница {page_num}: {url}")
        html = fetch_page(url)
        products, next_url = parse_books_page(html, current_url=url)
        print(f"  найдено книг: {len(products)}")
        all_products.extend(products)
        url = next_url

    print(f"[Books] Всего собрано книг: {len(all_products)}")
    return all_products


def scrape_laptops():
    """
    Скрапит ноутбуки с demo-сайта WebScraper.
    """
    print(f"[Laptops] Загружаю: {LAPTOPS_URL}")
    html = fetch_page(LAPTOPS_URL)
    products = parse_laptops_page(html, base_url=LAPTOPS_URL)
    print(f"[Laptops] Найдено ноутбуков: {len(products)}")
    return products


def main():
    parser = argparse.ArgumentParser(
        description="Демо-парсер цен (Books to Scrape + WebScraper Laptops)."
    )
    parser.add_argument(
        "--max-book-pages",
        type=int,
        default=2,
        help="Сколько страниц книг скачивать (по умолчанию 2). Всего там 50.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Путь к CSV (по умолчанию {DEFAULT_OUTPUT}).",
    )
    parser.add_argument(
        "--no-analyze",
        action="store_true",
        help="Не печатать аналитику после сбора.",
    )

    args = parser.parse_args()

    # 1) Книги
    books = scrape_books(max_pages=args.max_book_pages)

    # 2) Ноутбуки
    laptops = scrape_laptops()

    # 3) Сохранение
    all_products = books + laptops
    if not all_products:
        print("Ничего не удалось собрать — проверь подключение к интернету.")
        return

    save_products_to_csv(all_products, args.output)
    print(f"\nСохранено {len(all_products)} записей в {args.output}")

    # 4) Аналитика
    if not args.no_analyze:
        print("\n=== Аналитика ===")
        print_basic_stats(args.output)


if __name__ == "__main__":
    main()
