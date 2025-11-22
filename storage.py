# storage.py
from typing import List
from pathlib import Path
from datetime import datetime

import pandas as pd

from parsers import Product


def save_products_to_csv(products: List[Product], path: str) -> None:
    """
    Сохраняет список продуктов в CSV.
    Если файл уже есть — дописывает строки без заголовка.
    """
    if not products:
        return

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().isoformat(timespec="seconds")

    rows = []
    for p in products:
        rows.append(
            {
                "name": p.name,
                "price": p.price,
                "currency": p.currency,
                "source": p.source,
                "url": p.url,
                "scraped_at": now,
            }
        )

    df = pd.DataFrame(rows)

    if output_path.exists():
        df.to_csv(output_path, mode="a", header=False, index=False, encoding="utf-8")
    else:
        df.to_csv(output_path, index=False, encoding="utf-8")
