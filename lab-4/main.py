import json

def load_scenario_from_json():
    """
    Завантажує сценарій тестування з JSON-файлу.
    Повертає альтернативи, експертів та матрицю ранжувань.
    JSON має містити ключі: "alternatives", "experts" та "rankings".
    """
    file_path = 'test.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            alternatives = data.get("alternatives", [])
            experts = data.get("experts", [])
            rankings = data.get("rankings", [])
            if not alternatives:
                print("Не знайдено альтернатив у файлі.")
            if not experts:
                print("Не знайдено експертів у файлі.")
            if not rankings:
                print("Не знайдено ранжувань у файлі.")
            return alternatives, experts, rankings
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
    except json.JSONDecodeError:
        print(f"Помилка при зчитуванні JSON з файлу {file_path}.")
    return [], [], []


def input_scenario_manually():
    """
    Дозволяє користувачеві ввести сценарій вручну.
    Повертає альтернативи, експертів та матрицю ранжувань.
    """
    n, alternatives = input_number_of_alternatives()
    experts = input_experts()
    rankings_matrix = input_rankings(alternatives, experts)
    return alternatives, experts, rankings_matrix


def input_number_of_alternatives():
    """
    Запитує число альтернативних рішень.
    Повертає число альтернатив та список назв (A1, A2, ...).
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
    alternatives = [f"A{i + 1}" for i in range(n)]
    return n, alternatives


def input_experts():
    """
    Запитує число експертів та їх імена.
    Повертає список імен експертів.
    """
    while True:
        try:
            m = int(input("Введіть число експертів: "))
            if m <= 0:
                print("Число експертів має бути додатнім.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть ціле число.")
    experts = []
    for i in range(m):
        name = input(f"Введіть ім'я експерта {i + 1}: ").strip()
        if not name:
            name = f"Експерт_{i + 1}"
        experts.append(name)
    return experts


def input_rankings(alternatives, experts):
    """
    Послідовно вводить дані ранжування для кожного експерта.
    Ранжування має бути числом від 1 до кількості альтернатив.
    Повертає матрицю ранжувань, де кожен рядок відповідає альтернативі,
    а стовпці – експертам.
    """
    n = len(alternatives)
    expert_rankings = []
    for expert in experts:
        print(f"\nВведіть ранжування для експерта {expert}:")
        rankings = []
        for alt in alternatives:
            while True:
                try:
                    rank = int(input(f"  Ранг для {alt} (від 1 до {n}): "))
                    if 1 <= rank <= n:
                        rankings.append(rank)
                        break
                    else:
                        print(f"  Ранг має бути між 1 та {n}.")
                except ValueError:
                    print("  Некоректне значення. Введіть ціле число.")
        expert_rankings.append(rankings)
    rankings_matrix = [list(row) for row in zip(*expert_rankings)]
    return rankings_matrix


def print_ranking_table(alternatives, experts, matrix):
    """
    Виводить таблицю з даними початкових ранжувань.
    Перший стовпець – назва альтернативи, наступні – ранги експертів.
    """
    header = ["Альтернатива"] + experts
    rows = [header]
    for alt, ranks in zip(alternatives, matrix):
        row = [alt] + [str(rank) for rank in ranks]
        rows.append(row)

    col_widths = [max(len(row[i]) for row in rows) for i in range(len(header))]
    print("\nТаблиця початкових ранжувань:")
    for row in rows:
        formatted_row = "  ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row))
        print(formatted_row)


def is_dominated(rank_i, rank_j):
    """
    Перевіряє, чи альтернатива з рейтингом rank_j домінує над альтернативою з рейтингом rank_i.
    Домінування означає, що для всіх експертів: rank_j <= rank_i і хоча б для одного – строго менше.
    """
    less_or_equal = all(rj <= ri for ri, rj in zip(rank_i, rank_j))
    strictly_less = any(rj < ri for ri, rj in zip(rank_i, rank_j))
    return less_or_equal and strictly_less


def determine_pareto_set(matrix):
    """
    Визначає множину Парето оптимальних рішень.
    Повертає список індексів альтернатив, які не доміновані іншими.
    """
    n = len(matrix)
    dominated = [False] * n
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if is_dominated(matrix[i], matrix[j]):
                dominated[i] = True
                break
    pareto_indices = [i for i, dom in enumerate(dominated) if not dom]
    return pareto_indices


def print_pareto_set(alternatives, pareto_indices):
    """
    Виводить множину Парето оптимальних рішень.
    """
    if pareto_indices:
        pareto_alts = [alternatives[i] for i in pareto_indices]
        print("\nМножина Парето оптимальних рішень:")
        print(", ".join(pareto_alts))
    else:
        print("\nНемає Парето оптимальних рішень.")


def main():
    print("Метод прямого перебору для побудови множини Парето\n")
    use_json = input("Бажаєте завантажити сценарій з JSON файлу? (y/n): ").strip().lower()

    if use_json == "y":
        alternatives, experts, rankings_matrix = load_scenario_from_json()
        if not (alternatives and experts and rankings_matrix):
            print("Неповні або некоректні дані в файлі. Завершення роботи.")
            return
    else:
        alternatives, experts, rankings_matrix = input_scenario_manually()

    print_ranking_table(alternatives, experts, rankings_matrix)
    pareto_indices = determine_pareto_set(rankings_matrix)
    print_pareto_set(alternatives, pareto_indices)


if __name__ == "__main__":
    main()
