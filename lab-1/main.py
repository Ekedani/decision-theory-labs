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
            n_experts = int(input("\nВведіть кількість експертів: "))
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
    Запитує систему балів (наприклад, '10' для десятибальної системи).
    Повертає максимальне значення балів як число (int).
    """
    while True:
        scoring_input = input("\nВведіть систему балів (наприклад, '10' для десятибальної системи): ").strip()
        try:
            scoring_max = float(scoring_input)
            if scoring_max <= 0:
                print("Система балів повинна бути додатнім числом.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Будь ласка, введіть число.")
    return scoring_max


def input_scores(experts, alternatives, scoring_max):
    """
    Опитування експертів: для кожного експерта запитуються оцінки для кожної альтернативи.
    Якщо введене значення не є числом, або знаходиться поза межами [0, scoring_max],
    то воно нормалізується (значення нижче 0 стає 0, вище scoring_max — scoring_max).
    Повертає матрицю оцінок (список списків).
    """
    scores = []
    for expert in experts:
        print(f"\nВведіть оцінки експерта {expert} (система: {scoring_max} балів):")
        expert_scores = []
        for alt in alternatives:
            while True:
                try:
                    score_input = input(f"  Оцінка для альтернативи '{alt}': ")
                    score = float(score_input)
                    if score < 0:
                        score = 0.0
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

    alternatives = input_alternatives()
    experts = input_experts()
    scoring_system = input_scoring_system()

    scores = input_scores(experts, alternatives, scoring_system)
    display_raw_scores(experts, alternatives, scores)

    normalized_scores = compute_normalized_scores(scores, len(experts), len(alternatives))
    ranked = rank_alternatives(alternatives, normalized_scores)
    display_ranked_alternatives(ranked)


if __name__ == "__main__":
    main()
