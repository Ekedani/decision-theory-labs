import json


def load_scenario_from_json(file_path):
    """
    Завантажує сценарій тестування з JSON-файлу.
    Повертає альтернативи, стани, систему оцінок та оцінки.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            alternatives = data.get('alternatives', [])
            states = data.get('states', [])
            scoring_min = data.get('scoring_min', 1)
            scoring_max = data.get('scoring_max', 10)
            scores = data.get('scores', [])
            return alternatives, states, scoring_min, scoring_max, scores
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
    except json.JSONDecodeError:
        print(f"Помилка при зчитуванні JSON з файлу {file_path}.")
    return [], [], 1, 10, []


def input_scenario_manually():
    """
    Дозволяє користувачеві ввести сценарій вручну.
    Повертає альтернативи, стани, систему оцінок та оцінки.
    """
    alternatives = input_alternatives()
    states = input_states()
    scoring_min, scoring_max = input_scoring_system()
    scores = input_scores(alternatives, states, scoring_min, scoring_max)
    return alternatives, states, scoring_min, scoring_max, scores


def input_alternatives():
    """
    Запитує кількість альтернатив.
    Повертає список альтернатив.
    """
    while True:
        try:
            n = int(input("Введіть число альтернативних рішень: "))
            if n <= 0:
                print("Число альтернатив має бути додатнім.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть ціле число.")
    return [f"A{i + 1}" for i in range(n)]


def input_states():
    """
    Запитує число зовнішніх умов (станів).
    Повертає список зовнішніх умов (станів).
    """
    while True:
        try:
            m = int(input("Введіть число зовнішніх умов (станів): "))
            if m <= 0:
                print("Число зовнішніх умов має бути додатнім.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть ціле число.")
    return [f"X{i + 1}" for i in range(m)]


def input_scoring_system():
    """
    Запитує систему балів: мінімальну та максимальну оцінку.
    Якщо користувач нічого не введе, використовуються значення за замовчуванням 1 та 10.
    """
    while True:
        scoring_min_input = input("Введіть мінімальну оцінку (за замовчуванням 1): ").strip()
        scoring_max_input = input("Введіть максимальну оцінку (за замовчуванням 10): ").strip()
        try:
            scoring_min = float(scoring_min_input) if scoring_min_input else 1.0
            scoring_max = float(scoring_max_input) if scoring_max_input else 10.0
            if scoring_min >= scoring_max:
                print("Мінімальна оцінка має бути меншою за максимальну.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть числа.")
    return scoring_min, scoring_max


def input_scores(alternatives, states, scoring_min, scoring_max):
    """
    Послідовно вводить значення корисності для кожної альтернативи та кожного стану.
    Якщо введене значення не є числом або знаходиться поза межами [scoring_min, scoring_max],
    то воно нормалізується (значення менше scoring_min замінюється на scoring_min, більше scoring_max – на scoring_max).
    Повертає матрицю оцінок як список списків.
    """
    scores = []
    print("\nВведіть значення корисності для кожної альтернативи та кожного стану:")
    for alt in alternatives:
        row = []
        for state in states:
            while True:
                try:
                    score_input = input(f"  Оцінка для {alt} при {state} (від {scoring_min} до {scoring_max}): ")
                    value = float(score_input)
                    if value < scoring_min:
                        value = scoring_min
                        print(f"  Значення менше за мінімальне. Буде використано значення {scoring_min}")
                    elif value > scoring_max:
                        value = scoring_max
                        print(f"  Значення більше за максимальне. Буде використано значення {scoring_max}")
                    row.append(value)
                    break
                except ValueError:
                    print("  Некоректне значення, спробуйте ще раз. Будь ласка, введіть число.")
        scores.append(row)
    return scores


def choose_criterion():
    """
    Дозволяє користувачеві вибрати критерій:
      1 – критерій Севіджа,
      2 – критерій Лапласа.
    Повертає рядок: "Sevidge" або "Laplace".
    """
    while True:
        print("\nОберіть критерій:")
        print("  1 – критерій Севіджа (мінімізація максимального жалю)")
        print("  2 – критерій Лапласа (максимізація середнього виграшу)")
        choice = input("Ваш вибір (1 або 2): ").strip()
        if choice == "1":
            return "sevidge"
        elif choice == "2":
            return "laplace"
        else:
            print("Некоректний вибір. Будь ласка, введіть 1 або 2.")


def calculate_sevidge(matrix):
    """
    Розраховує критерій Севіджа.
    Для кожного стовпця знаходиться максимальне значення, а потім для кожного елемента
    обчислюється 'жалю' як різниця: max_j - a_ij.
    Критерій для альтернативи – максимальне значення жалю по всіх станах.
    Повертає список значень критерію для кожної альтернативи.
    """
    if not matrix or not matrix[0]:
        return []
    num_alts = len(matrix)
    num_states = len(matrix[0])
    max_in_states = [max(matrix[i][j] for i in range(num_alts)) for j in range(num_states)]
    sevidge_values = []
    for i in range(num_alts):
        regrets = [max_in_states[j] - matrix[i][j] for j in range(num_states)]
        sevidge_values.append(max(regrets))
    return sevidge_values


def calculate_laplace(matrix):
    """
    Розраховує критерій Лапласа.
    Для кожної альтернативи обчислюється середній виграш (сума оцінок поділена на число станів).
    Повертає список середніх виграшів для кожної альтернативи.
    """
    if not matrix or not matrix[0]:
        return []
    num_states = len(matrix[0])
    laplace_values = [sum(row) / num_states for row in matrix]
    return laplace_values


def assign_ranks(criteria_values, descending=False):
    """
    Призначає ранги альтернативам за значенням критерію.
    Якщо descending = False, то кращим вважається менше значення (для Севіджа),
    а якщо descending = True – більше значення (для Лапласа).
    Найкраща альтернатива отримує ранг 1.
    Повертає список рангів, що відповідають позиціям альтернатив.
    """
    n = len(criteria_values)
    if descending:
        sorted_indices = sorted(range(n), key=lambda i: criteria_values[i], reverse=True)
    else:
        sorted_indices = sorted(range(n), key=lambda i: criteria_values[i])
    ranks = [0] * n
    for rank, idx in enumerate(sorted_indices, start=1):
        ranks[idx] = rank
    return ranks


def print_result_table(alternatives, states, matrix, criteria_values, ranks, criterion_label):
    """
    Виводить таблицю початкових значень (матрицю корисності) зі стовпчиком
    обчислених значень обраного критерію та стовпчиком з рангами.
    """
    header = ["Альтернатива"] + states + [f"Критерій {criterion_label}", "Ранг"]
    rows = [header]

    for i, alt in enumerate(alternatives):
        row_values = [f"{val:.2f}" for val in matrix[i]]
        crit_val = f"{criteria_values[i]:.2f}"
        row = [alt] + row_values + [crit_val, str(ranks[i])]
        rows.append(row)

    global_width = max(len(cell) for row in rows for cell in row)
    print("\nРезультати:")
    for row in rows:
        formatted_row = "  ".join(cell.center(global_width) for cell in row)
        print(formatted_row)


def main():
    print('Критерії Севіджа і Лапласа\n')

    use_json = input("Бажаєте завантажити сценарій з JSON файлу? (y/n): ").strip().lower()

    if use_json == 'y':
        alternatives, states, scoring_min, scoring_max, scores = load_scenario_from_json('test.json')

        if not (alternatives and states and scores):
            print("Неповні або некоректні дані в файлі. Перевірте формат JSON.")
            return
    else:
        alternatives, states, scoring_min, scoring_max, scores = input_scenario_manually()

    criteria = choose_criterion()

    if criteria == "sevidge":
        crit_values = calculate_sevidge(scores)
        ranks = assign_ranks(crit_values, descending=False)
        criterion_label = "Севіджа"
    else:
        crit_values = calculate_laplace(scores)
        ranks = assign_ranks(crit_values, descending=True)
        criterion_label = "Лапласа"

    print_result_table(alternatives, states, scores, crit_values, ranks, criterion_label)


if __name__ == "__main__":
    main()
