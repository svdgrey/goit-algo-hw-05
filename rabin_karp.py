# Алгоритм пошуку підрядка Рабіна-Карпа.

# Обчислює поліноміальний хеш рядка s.
# - s: рядок для хешування
# - base: базове число для хешування (за замовчуванням 256)
# - modulus: модуль для обчислення хешу (за замовчуванням 101)
# Повертає поліноміальний хеш рядка s.  
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0

    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (
            hash_value + ord(char) * power_of_base
        ) % modulus

    return hash_value

# Виконує пошук підрядка за алгоритмом Рабіна-Карпа.
# - main_string: текст, у якому виконується пошук
# - substring: підрядок для пошуку
# Повертає індекс першого входження або -1. 
def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101

    # Хеш-значення для підрядка пошуку та поточного відрізка
    substring_hash = polynomial_hash(
        substring, base, modulus
    )
    current_slice_hash = polynomial_hash(
        main_string[:substring_length], base, modulus
    )

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(
        base, substring_length - 1
    ) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash
                - ord(main_string[i]) * h_multiplier
            ) % modulus

            current_slice_hash = (
                current_slice_hash * base
                + ord(main_string[i + substring_length])
            ) % modulus

            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1
