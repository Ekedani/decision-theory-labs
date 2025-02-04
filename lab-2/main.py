def input_alternatives():
    """
    Запитує кількість альтернатив та їх імена.
    Повертає список альтернатив.
    """
    while True:
        try:
            n_alternatives = int(input("Введіть кількість альтернатив: "))
            if n_alternatives <= 0:
                print("Кількість альтернатив повинна бути додатнім числом.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть ціле число.")

    alternatives = []
    for i in range(n_alternatives):
        alt_name = input(f"Введіть назву альтернативи {i + 1}: ").strip()
        if not alt_name:
            alt_name = f"a{i + 1}"
        alternatives.append(alt_name)
    return alternatives


def input_states():
    """
    Запитує кількість зовнішніх умов (станів) та їх імена.
    Повертає список зовнішніх умов (станів).
    """
    while True:
        try:
            n_states = int(input("\nВведіть кількість зовнішніх умов (станів): "))
            if n_states <= 0:
                print("Кількість зовнішніх умов (станів) повинна бути додатнім числом.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть ціле число.")

    states = []
    for i in range(n_states):
        state_name = input(f"Введіть ім'я стану {i + 1}: ").strip()
        if not state_name:
            state_name = f"X{i + 1}"
        states.append(state_name)
    return states


def input_scoring_system():
    """
    Запитує систему балів: мінімальну та максимальну оцінку.
    Якщо нічого не введено, використовується значення за замовчуванням: мінімум 1, максимум 10.
    Повертає кортеж (scoring_min, scoring_max).
    """
    while True:
        scoring_min_input = input("\nВведіть мінімальну оцінку (за замовчуванням 1): ").strip()
        scoring_max_input = input("Введіть максимальну оцінку (за замовчуванням 10): ").strip()
        try:
            scoring_min = float(scoring_min_input) if scoring_min_input else 1.0
            scoring_max = float(scoring_max_input) if scoring_max_input else 10.0
            if scoring_min >= scoring_max:
                print("Мінімальна оцінка повинна бути меншою за максимальну. Спробуйте ще раз.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть числа.")
    return scoring_min, scoring_max


def main():
    print('Критерії прийняття рішень в умовах невизначеності')

    alternatives = input_alternatives()
    states = input_states()
    scoring_min, scoring_max = input_scoring_system()


if __name__ == "__main__":
    main()
