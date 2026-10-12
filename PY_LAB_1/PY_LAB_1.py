# Програма для аналізу температурних показів за день

print("=== Аналіз температурних показів за день ===")
print("Введіть до 24 значень температур (через пробіл):")

# Введення температур користувачем
temp_input = input("Температури: ").strip()

# Перевірка кількості значень
if not temp_input:
    print("[!] Помилка: Введено порожній рядок.")
    exit()

temp_strings = temp_input.split()
if len(temp_strings) > 24:
    print(f"[!] Помилка: Кількість вимірювань ({len(temp_strings)}) перевищує максимально допустиму (24).")
    exit()

# Створення та наповнення списку для числових значень показів температур
temperatures = []
for t_str in temp_strings:
    try:
        val = float(t_str)
        if -40 <= val <= 40:
            temperatures.append(val)
        else:
            print(f"[!] Помилка: Значення {val} виходить за межі допустимого діапазону (-40..40).")
            exit()
    except ValueError:
        print(f"[!] Помилка: '{t_str}' не є коректним числом.")
        exit()

# Перевірка, чи додались у список хоч якісь дані (список с числовими показами містить значення), інакше завершити програму
if len(temperatures) < 2:
    print("[!] Помилка: Потрібно ввести щонайменше два температурних показники для проведення аналізу.")
    exit()

# Введення часових міток
print("\nВведіть часові мітки для кожного показу (у форматі 'година:хвилина') через пробіл:")
time_input = input("Мітки часу: ").strip()
time_strings = time_input.split()

# Перевірка формату часу
validated_times = []
for t_str in time_strings:
    parts = t_str.split(':')
    if len(parts) != 2:
        print(f"[!] Помилка: Неправильний формат часу '{t_str}'. Використовуйте 'година:хвилина'.")
        exit()
    try:
        hour = int(parts[0])
        minute = int(parts[1])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            validated_times.append(t_str)
        else:
            print(f"[!] Помилка: Час '{t_str}' містить неприпустимі значення (години: 0-23, хвилини: 0-59).")
            exit()
    except ValueError:
        print(f"[!] Помилка: Час '{t_str}' містить нечислові символи.")
        exit()

# Перевірка кількості міток
if len(validated_times) != len(temperatures):
    print(f"[!] Помилка: Кількість міток часу ({len(validated_times)}) не збігається з кількістю температур ({len(temperatures)}).")
    exit()

# Створення словника {час: температура, час: температура, ...}
temp_dict = {}
for i in range(len(temperatures)):
    temp_dict[validated_times[i]] = temperatures[i]


# === Обчислення характеристик через словник з даними ===
# а) виділити значення та ключі зі словника
times_list = list(temp_dict.keys())
temps_list = list(temp_dict.values())

# б) розрахувати середнє значення
avg_temp = sum(temps_list) / len(temps_list)

# в) розрахувати мінімум та максимум
max_temp = max(temps_list)
min_temp = min(temps_list)

# г) розрахувати кількість позитивних та негативних температур
positive_count = sum(1 for t in temps_list if t > 0)
negative_count = sum(1 for t in temps_list if t < 0)

# д) зробити виявлення різких змін: зробити список, в якому зберігати кортеж-діапазон часових міток, між якими стався різкий перепад температур (>7 градусів), та різниці температур (час1, час2, різниця)
sudden_changes = []
for i in range(len(temps_list) - 1):
    diff = abs(temps_list[i+1] - temps_list[i])
    if diff > 7:
        sudden_changes.append((times_list[i], times_list[i+1], diff))


# === Виведення результатів ===
print("\n=== РЕЗУЛЬТАТ АНАЛІЗУ ===")
print("Температурні дані (час → температура):")
# а) вивести усі покази у форматі "часова мітка" - "значення температури" зі словника
for time_key, temp_val in temp_dict.items():
    print(f"   {time_key} → {temp_val:6.1f} °C")

# б) вивести отримані числові значення статистичних показників
print(f"\nЗагальна кількість вимірювань: {len(temp_dict)}")
print(f"Середня температура: {avg_temp:.2f} °C")
print(f"Максимальна температура: {max_temp:.1f} °C")
print(f"Мінімальна температура: {min_temp:.1f} °C")
print(f"Кількість додатних температур: {positive_count}")
print(f"Кількість від’ємних температур: {negative_count}")

# Виведення різких змін
if sudden_changes:
    print("\n[!] Виявлено різкі зміни температури (> 7°):")
    for t1, t2, diff in sudden_changes:
        print(f"  між {t1} та {t2}: зміна на {diff:.1f}°C")
else:
    print("\n[i] Різких змін температур (> 7°) не виявлено.")

print("\n=== Кінець аналізу ===")
