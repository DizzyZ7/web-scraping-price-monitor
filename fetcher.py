# fetcher.py
import requests
from typing import Optional, Dict, Any

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}


def fetch_page(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 15,
) -> str:
    """
    Загружает HTML-страницу по URL.
    Поднимает исключение, если код ответа не 2xx.
    """
    resp = requests.get(url, headers=DEFAULT_HEADERS, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.text
