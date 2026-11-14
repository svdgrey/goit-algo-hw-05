# Реалізація алгоритму пошуку підрядка Боєра-Мура.

# Створює таблицю зсувів для алгоритму Боєра-Мура.
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)

    # Для кожного символу в підрядку встановлюємо зсув
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    # Якщо символу немає в таблиці, зсув дорівнює довжині
    table.setdefault(pattern[-1], length)

    return table

# Виконує пошук підрядка в тексті за алгоритмом Боєра-Мура.
# - text: текст для пошуку
# - pattern: підрядок для пошуку
# Повертає індекс першого входження підрядка або -1, якщо не знайдено. 
def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для підрядка
    shift_table = build_shift_table(pattern)
    i = 0

    # Проходимо по основному тексту
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        # Порівнюємо символи справа наліво
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        # Підрядок знайдено
        if j < 0:
            return i

        # Зсуваємо індекс на основі таблиці зсувів
        i += shift_table.get(
            text[i + len(pattern) - 1],
            len(pattern)
        )

    return -1
