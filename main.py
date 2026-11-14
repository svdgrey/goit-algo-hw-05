
import timeit
from pathlib import Path

from matplotlib import text
from tabulate import tabulate

from boyer_moore import boyer_moore_search
from kmp_search import kmp_search
from rabin_karp import rabin_karp_search


REPEAT_COUNT = 100
MEASUREMENTS = 5

ARTICLES_DIR = Path(__file__).resolve().parent / "articles"

ARTICLES = [
    ARTICLES_DIR / "стаття 1.txt",
    ARTICLES_DIR / "стаття 2.txt",
]

ALGORITHMS = {
    "Boyer-Moore": boyer_moore_search,
    "KMP": kmp_search,
    "Rabin-Karp": rabin_karp_search,
}

# Вибирає існуючий та відсутній підрядки.
# - text: текст статті
def get_patterns(text: str) -> tuple[str, str]:
    if not text:
        raise ValueError("Текст статті порожній")

    missing = "Єхидна, ґава, їжак ще й шиплячі плазуни бігцем форсують Янцзи"
    length = len(missing)

    start = (len(text) - length) // 2
    existing = text[start:start + length]

    while missing in text:
        missing += "§"

    return existing, missing


# Вимірює час одного пошуку в мілісекундах.
# - search_function: алгоритм пошуку
# - text: текст статті
# - pattern: підрядок для пошуку
def measure_search(search_function, text: str, pattern: str) -> float:
    times = timeit.repeat(
        lambda: search_function(text, pattern),
        repeat=MEASUREMENTS,
        number=REPEAT_COUNT,
    )

    return min(times) / REPEAT_COUNT * 1000


# Виконує вимірювання для всіх алгоритмів та статей.
def benchmark() -> list[dict]:
    results = []

    for article in ARTICLES:
        text = article.read_text(encoding="utf-8-sig")
        existing, missing = get_patterns(text)

        print(f"\nСтаття: {article.name}")
        print(f"Довжина тексту: {len(text)}")
        print(f"Існуючий підрядок: {existing!r}")
        print(f"Відсутній підрядок: {missing!r}")

        for pattern_type, pattern in [
            ("Існує", existing),
            ("Відсутній", missing),
        ]:
            expected = text.find(pattern)

            for name, algorithm in ALGORITHMS.items():
                # Перевіряємо правильність пошуку
                assert algorithm(text, pattern) == expected, (
                    f"Помилка алгоритму: {name}"
                )

                elapsed = measure_search(
                    algorithm, text, pattern
                )

                results.append({
                    "article": article.name,
                    "pattern_type": pattern_type,
                    "algorithm": name,
                    "time_ms": elapsed,
                })

    return results


# Виводить таблиці та визначає найшвидші алгоритми.
def main():
    try:
        results = benchmark()

    except (OSError, UnicodeError, ValueError) as error:
        print(f"Помилка: {error}")
        return


    print()
    print("Параметри тестування:")
    print(f"Кількість серій вимірювань: {MEASUREMENTS}")
    print(f"Кількість повторень у серії: {REPEAT_COUNT}")
    print(f"Загальна кількість пошуків на один тест: {MEASUREMENTS * REPEAT_COUNT}")
    print()

    for article in ARTICLES:
        article_results = [
            result for result in results
            if result["article"] == article.name
        ]

        rows = [
            [
                result["pattern_type"],
                result["algorithm"],
                result["time_ms"],
            ]
            for result in article_results
        ]

        print(f"\nРезультати: {article.name}")
        print(tabulate(
            rows,
            headers=["Підрядок", "Алгоритм", "Час (мс)"],
            tablefmt="github",
            floatfmt=".6f",
        ))

        # Сумарний час для кожного алгоритму в статті
        totals = {
            name: sum(
                result["time_ms"]
                for result in article_results
                if result["algorithm"] == name
            )
            for name in ALGORITHMS
        }

        fastest = min(totals, key=totals.get)
        print(f"Найшвидший алгоритм для '{article.name}': {fastest}")

    # Загальне порівняння для обох статей
    totals = {
        name: sum(
            result["time_ms"]
            for result in results
            if result["algorithm"] == name
        )
        for name in ALGORITHMS
    }

    print("\nЗагальні результати:")
    print(tabulate(
        totals.items(),
        headers=["Алгоритм", "Сумарний час (мс)"],
        tablefmt="github",
        floatfmt=".6f",
    ))

    fastest = min(totals, key=totals.get)
    print(f"\nНайшвидший алгоритм загалом: {fastest}")


if __name__ == "__main__":
    main()
