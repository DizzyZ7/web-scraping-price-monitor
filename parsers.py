# parsers.py
from dataclasses import dataclass
from typing import List, Tuple, Optional
from urllib.parse import urljoin
import re

from bs4 import BeautifulSoup


@dataclass
class Product:
    name: str
    price: float
    currency: str
    source: str   # "books" или "laptops"
    url: str


def _extract_price(text: str) -> Optional[float]:
    """
    Достаёт число из строки с ценой.
    Примеры:
      '£51.77'  -> 51.77
      '$295.99' -> 295.99
    """
    # Оставляем только цифры и точку
    cleaned = re.sub(r"[^0-9.]", "", text)
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


# ---------- Books to Scrape ----------

def parse_books_page(html: str, current_url: str) -> Tuple[List[Product], Optional[str]]:
    """
    Парсит страницу https://books.toscrape.com/ (или page-2.html и т.п.)
    Возвращает:
      - список Product
      - URL следующей страницы (или None)
    """
    soup = BeautifulSoup(html, "html.parser")
    products: List[Product] = []

    # Каждая книга в article.product_pod
    for art in soup.select("article.product_pod"):
        # Заголовок и ссылка
        a = art.select_one("h3 > a")
        if not a:
            continue

        # На этом сайте title в атрибуте title
        name = a.get("title") or a.get_text(strip=True)
        rel_href = a.get("href", "")
        url = urljoin(current_url, rel_href)

        # Цена
        price_el = art.select_one("p.price_color")
        if not price_el:
            continue
        price = _extract_price(price_el.get_text(strip=True))
        if price is None:
            continue

        products.append(
            Product(
                name=name,
                price=price,
                currency="GBP",
                source="books",
                url=url,
            )
        )

    # Пагинация: <li class="next"><a href="page-2.html">next</a></li>
    next_link = soup.select_one("li.next > a")
    next_url = None
    if next_link and next_link.get("href"):
        next_url = urljoin(current_url, next_link["href"])

    return products, next_url


# ---------- WebScraper demo (laptops) ----------

def parse_laptops_page(html: str, base_url: str) -> List[Product]:
    """
    Парсит страницу:
      https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops

    Берём:
      - цену из <h4 class="pull-right price">
      - имя и ссылку из <a class="title">
    """
    soup = BeautifulSoup(html, "html.parser")
    products: List[Product] = []

    # Каждая карточка: <div class="col-sm-4 col-lg-4 col-md-4">
    cards = soup.find_all("div", class_="col-sm-4 col-lg-4 col-md-4")

    for card in cards:
        title_a = card.select_one("a.title")
        price_h4 = card.select_one("h4.price")

        if not title_a or not price_h4:
            # Попробуем более общий вариант
            if not title_a:
                title_a = card.find("a")
            if not price_h4:
                price_h4 = card.find("h4", class_="pull-right")

        if not title_a or not price_h4:
            continue

        name = title_a.get_text(strip=True)
        price = _extract_price(price_h4.get_text(strip=True))
        if price is None:
            continue

        rel_href = title_a.get("href", "")
        url = urljoin(base_url, rel_href)

        products.append(
            Product(
                name=name,
                price=price,
                currency="USD",
                source="laptops",
                url=url,
            )
        )

    return products
