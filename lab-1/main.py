import json


def load_scenario_from_json(file_path):
    """
    Завантажує сценарій тестування з JSON-файлу.
    Повертає альтернативи, експертів, систему оцінок і оцінки.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            alternatives = data.get('alternatives', [])
            experts = data.get('experts', [])
            scoring_min = data.get('scoring_min', 0)
            scoring_max = data.get('scoring_max', 10)
            scores = data.get('scores', [])
            return alternatives, experts, scoring_min, scoring_max, scores
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
    except json.JSONDecodeError:
        print(f"Помилка при зчитуванні JSON з файлу {file_path}.")
    return [], [], 0, 10, []


def input_scenario_manually():
    """
    Дозволяє користувачеві ввести сценарій вручну.
    Повертає альтернативи, експертів, систему оцінок і оцінки.
    """
    alternatives = input_alternatives()
    experts = input_experts()
    scoring_min, scoring_max = input_scoring_system()
    scores = input_scores(experts, alternatives, scoring_min, scoring_max)
    return alternatives, experts, scoring_min, scoring_max, scores


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


def input_experts():
    """
    Запитує кількість експертів та їх імена.
    Повертає список експертів.
    """
    while True:
        try:
            n_experts = int(input("Введіть кількість експертів: "))
            if n_experts <= 0:
                print("Кількість експертів повинна бути додатнім числом.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть ціле число.")

    experts = []
    for i in range(n_experts):
        expert_name = input(f"Введіть ім'я експерта {i + 1}: ").strip()
        if not expert_name:
            expert_name = f"E{i + 1}"
        experts.append(expert_name)
    return experts


def input_scoring_system():
    """
    Запитує систему балів: мінімальну та максимальну оцінку.
    Якщо нічого не введено, використовується значення за замовчуванням: мінімум 0, максимум 10.
    Повертає кортеж (scoring_min, scoring_max).
    """
    while True:
        scoring_min_input = input("Введіть мінімальну оцінку (за замовчуванням 0): ").strip()
        scoring_max_input = input("Введіть максимальну оцінку (за замовчуванням 10): ").strip()
        try:
            scoring_min = float(scoring_min_input) if scoring_min_input else 0.0
            scoring_max = float(scoring_max_input) if scoring_max_input else 10.0
            if scoring_min >= scoring_max:
                print("Мінімальна оцінка повинна бути меншою за максимальну. Спробуйте ще раз.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть числа.")
    return scoring_min, scoring_max


def input_scores(experts, alternatives, scoring_min, scoring_max):
    """
    Опитування експертів: для кожного експерта запитуються оцінки для кожної альтернативи.
    Якщо введене значення не є числом або знаходиться поза межами [scoring_min, scoring_max],
    то воно нормалізується (значення менше scoring_min стає scoring_min, вище scoring_max — scoring_max).
    Повертає матрицю оцінок (список списків).
    """
    scores = []
    for expert in experts:
        print(f"\nВведіть оцінки експерта {expert} (система: від {scoring_min} до {scoring_max}):")
        expert_scores = []
        for alt in alternatives:
            while True:
                try:
                    score_input = input(f"  Оцінка для альтернативи '{alt}': ")
                    score = float(score_input)
                    if score < scoring_min:
                        score = scoring_min
                    elif score > scoring_max:
                        score = scoring_max
                    expert_scores.append(score)
                    break
                except ValueError:
                    print("Некоректне значення, спробуйте ще раз. Будь ласка, введіть число.")
        scores.append(expert_scores)
    return scores


def display_raw_scores(experts, alternatives, scores):
    """
    Виводить таблицю вихідних оцінок із підсумками для кожного експерта.
    """
    header = "Експерт".ljust(15) + "".join(alt.ljust(15) for alt in alternatives) + "Сума".ljust(15)
    print("\nТаблиця вихідних оцінок:")
    print(header)
    for expert, expert_scores in zip(experts, scores):
        row_sum = sum(expert_scores)
        row_str = expert.ljust(15)
        for score in expert_scores:
            row_str += str(score).ljust(15)
        row_str += str(row_sum).ljust(15)
        print(row_str)


def compute_normalized_scores(scores, n_experts, n_alternatives):
    """
    Обчислює нормовані оцінки:
    1. Для кожного експерта нормуємо його оцінки (ділимо на суму оцінок експерта).
    2. Для кожної альтернативи обчислюємо середнє значення нормованих оцінок по всіх експертах.

    Повертає список середніх нормованих оцінок для кожної альтернативи.
    """
    normalized_scores = [0] * n_alternatives
    for i in range(n_experts):
        row_sum = sum(scores[i])
        if row_sum == 0:
            normalized = [0] * n_alternatives
        else:
            normalized = [score / row_sum for score in scores[i]]
        for j in range(n_alternatives):
            normalized_scores[j] += normalized[j]

    normalized_scores = [ns / n_experts for ns in normalized_scores]
    return normalized_scores


def rank_alternatives(alternatives, normalized_scores):
    """
    Ранжує альтернативи за середніми нормованими оцінками за спаданням.
    Повертає список кортежів (альтернатива, нормована оцінка).
    """
    ranked = sorted(zip(alternatives, normalized_scores), key=lambda x: x[1], reverse=True)
    return ranked


def display_ranked_alternatives(ranked):
    """
    Виводить проранжовані альтернативи із зазначенням нормованих оцінок.
    """
    print("\nНормовані оцінки порівняльної переваги альтернатив:")
    print("Альтернатива".ljust(20) + "Нормована оцінка")
    for alt, norm_score in ranked:
        print(alt.ljust(20) + f"{norm_score:.4f}")


def main():
    print("Метод безпосередньої оцінки порівняльної переваги альтернатив\n")

    use_json = input("Бажаєте завантажити сценарій з JSON файлу? (y/n): ").strip().lower()

    if use_json == 'y':
        alternatives, experts, scoring_min, scoring_max, scores = load_scenario_from_json('test.json')

        if not (alternatives and experts and scores):
            print("Неповні або некоректні дані в файлі. Перевірте формат JSON.")
            return
    else:
        alternatives, experts, scoring_min, scoring_max, scores = input_scenario_manually()

    display_raw_scores(experts, alternatives, scores)
    normalized_scores = compute_normalized_scores(scores, len(experts), len(alternatives))
    ranked = rank_alternatives(alternatives, normalized_scores)
    display_ranked_alternatives(ranked)


if __name__ == "__main__":
    main()
