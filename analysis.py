# analysis.py
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def print_basic_stats(path: str, top_n: int = 10) -> None:
    """
    Простая аналитика:
      - кол-во записей
      - статистика по источникам
      - топ-N самых дешёвых товаров
    """
    df = load_data(path)

    if df.empty:
        print("Файл с данными пустой.")
        return

    print(f"Всего записей: {len(df)}")

    print("\nСредняя цена по источникам:")
    print(df.groupby("source")["price"].agg(["count", "min", "max", "mean"]))

    print(f"\nТоп-{top_n} самых дешёвых товаров:")
    cols = ["name", "price", "currency", "source", "url"]
    print(df.sort_values("price").head(top_n)[cols].to_string(index=False))
