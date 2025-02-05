import json


def load_scenario_from_json(file_path):
    """
    Завантажує сценарій тестування з JSON-файлу.
    Повертає альтернативи, стани, систему оцінок, ступінь оптимізму та оцінки.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            alternatives = data.get('alternatives', [])
            states = data.get('states', [])
            scoring_min = data.get('scoring_min', 1)
            scoring_max = data.get('scoring_max', 10)
            alpha = data.get('alpha', 0.5)
            scores = data.get('scores', [])
            return alternatives, states, scoring_min, scoring_max, alpha, scores
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
    except json.JSONDecodeError:
        print(f"Помилка при зчитуванні JSON з файлу {file_path}.")
    return [], [], 1, 10, 0.5, []


def input_scenario_manually():
    """
    Дозволяє користувачеві ввести сценарій вручну.
    Повертає альтернативи, стани, систему оцінок, ступінь оптимізму та оцінки.
    """
    alternatives = input_alternatives()
    states = input_states()
    scoring_min, scoring_max = input_scoring_system()
    alpha = input_alpha()
    scores = input_scores(alternatives, states, scoring_min, scoring_max)
    return alternatives, states, scoring_min, scoring_max, alpha, scores


def input_alternatives():
    """
    Запитує кількість альтернатив.
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
        alt_name = f"A{i + 1}"
        alternatives.append(alt_name)
    return alternatives


def input_states():
    """
    Запитує кількість зовнішніх умов (станів).
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


def input_alpha():
    """
    Запитує коефіцієнт оптимізму для критерію Гурвіца.
    Повертає значення alpha (число від 0 до 1).
    """
    while True:
        try:
            alpha = float(input(
                "\nВведіть коефіцієнт оптимізму (alpha) для критерію "
                "(від 0 до 1, де 0 => Макмакс, 1 => Вальда): "
            ).strip())
            if 0 <= alpha <= 1:
                return alpha
            print("Коефіцієнт має бути в діапазоні від 0 до 1.")
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть число від 0 до 1.")


def input_scores(alternatives, states, scoring_min, scoring_max):
    """
    Послідовно вводить значення корисності для кожної альтернативи та кожного стану.
    Повертає матрицю оцінок як список списків.
    """
    scores = []
    print("\nВведіть значення корисності для кожної альтернативи та кожного стану:")
    for alt in alternatives:
        row = []
        for state in states:
            while True:
                try:
                    score_input = input(f"  Введіть значення для {alt} при {state}: ")
                    value = float(score_input)
                    if value < scoring_min:
                        value = scoring_min
                    elif value > scoring_max:
                        value = scoring_max
                    row.append(value)
                    break
                except ValueError:
                    print("  Некоректне значення, спробуйте ще раз. Будь ласка, введіть число.")
        scores.append(row)
    return scores


def calculate_hurwicz(matrix, alpha):
    """
    Обчислює критерій Гурвіца для кожної альтернативи.

    Формула:
        H = alpha * (мінімальне значення) + (1 - alpha) * (максимальне значення)

    При:
      - alpha = 0.0: H = мінімальне значення (Вальда, песимістичний),
      - alpha = 1.0: H = максимальне значення (Макмакс, оптимістичний).

    Повертає список значень критерію для кожної альтернативи.
    """
    return [alpha * max(row) + (1 - alpha) * min(row) for row in matrix]


def assign_ranks(criteria_values):
    """
    Призначає ранги альтернативам за спаданням значення критерію.
    Найкраща альтернатива отримує ранг 1.
    Повертає список рангів, що відповідають позиціям альтернатив.
    """
    n = len(criteria_values)
    sorted_indices = sorted(range(n), key=lambda i: criteria_values[i], reverse=True)
    ranks = [0] * n
    for rank, idx in enumerate(sorted_indices, start=1):
        ranks[idx] = rank
    return ranks


def print_result_table(alternatives, states, scores, criteria_values, ranks, criterion_name):
    """
    Виводить таблицю початкових значень (матрицю корисності) зі стовпчиком
    обчислених значень критерію та стовпчиком з рангами.
    Покращене форматування: вирівнювання за шириною стовпців.
    """
    header = ["Альтернатива"] + states + [f"Критерій {criterion_name}", "Ранг"]

    rows = [header]
    for i in range(len(alternatives)):
        row = [alternatives[i]] + [f"{val:.2f}" for val in scores[i]] \
              + [f"{criteria_values[i]:.2f}", str(ranks[i])]
        rows.append(row)

    num_columns = len(header)
    col_widths = [max(len(row[col]) for row in rows) for col in range(num_columns)]

    for row in rows:
        formatted_row = "  ".join(word.ljust(col_widths[i]) for i, word in enumerate(row))
        print(formatted_row)


def main():
    print('Критерії прийняття рішень в умовах невизначеності\n')

    use_json = input("Бажаєте завантажити сценарій з JSON файлу? (y/n): ").strip().lower()

    if use_json == 'y':
        alternatives, states, scoring_min, scoring_max, alpha, scores = load_scenario_from_json('test.json')

        if not (alternatives and states and scores):
            print("Неповні або некоректні дані в файлі. Перевірте формат JSON.")
            return
    else:
        alternatives, states, scoring_min, scoring_max, alpha, scores = input_scenario_manually()

    if alpha == 0.0:
        criterion_name = "Вальда"
    elif alpha == 1.0:
        criterion_name = "Макмакс"
    else:
        criterion_name = f"Гурвіца (α = {alpha})"

    criteria_values = calculate_hurwicz(scores, alpha)
    ranks = assign_ranks(criteria_values)
    print_result_table(alternatives, states, scores, criteria_values, ranks, criterion_name)


if __name__ == "__main__":
    main()
