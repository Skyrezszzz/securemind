from sklearn.ensemble import RandomForestClassifier

# ==========================================
# ФУНКЦИЯ ИЗВЛЕЧЕНИЯ ПРИЗНАКОВ
# ==========================================

def extract_features(password):
    return [[
        len(password),
        int(any(c.isupper() for c in password)),
        int(any(c.islower() for c in password)),
        int(any(c.isdigit() for c in password)),
        int(any(not c.isalnum() for c in password))
    ]]

# ==========================================
# ОБУЧАЮЩИЕ ДАННЫЕ
# ==========================================

passwords = [
    "123456",
    "password",
    "qwerty",
    "admin",
    "welcome",
    "Qwerty123",
    "Hello2024",
    "Abc123!",
    "Secure@2025",
    "X9#kLm2@Pq"
]

labels = [
    0,  # слабый
    0,
    0,
    0,
    0,
    1,  # средний
    1,
    1,
    2,  # сильный
    2
]

X = []

for p in passwords:
    X.append([
        len(p),
        int(any(c.isupper() for c in p)),
        int(any(c.islower() for c in p)),
        int(any(c.isdigit() for c in p)),
        int(any(not c.isalnum() for c in p))
    ])

# ==========================================
# ОБУЧЕНИЕ МОДЕЛИ
# ==========================================

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, labels)

# ==========================================
# БАЗА СЛАБЫХ ПАРОЛЕЙ
# ==========================================

weak_passwords = [
    "123456",
    "password",
    "qwerty",
    "admin",
    "welcome",
    "12345678",
    "000000"
]

# ==========================================
# ВВОД ПОЛЬЗОВАТЕЛЯ
# ==========================================

password = input("Введите пароль: ")

# ==========================================
# ПРОВЕРКА НА ПОПУЛЯРНЫЕ ПАРОЛИ
# ==========================================

if password.lower() in weak_passwords:
    print("\n⚠ Пароль найден в базе популярных паролей!")

# ==========================================
# ПОДСЧЕТ НАДЕЖНОСТИ
# ==========================================

score = 0

if len(password) >= 12:
    score += 30
elif len(password) >= 8:
    score += 15

if any(c.isupper() for c in password):
    score += 20

if any(c.islower() for c in password):
    score += 10

if any(c.isdigit() for c in password):
    score += 20

if any(not c.isalnum() for c in password):
    score += 20

score = min(score, 100)

# ==========================================
# ПРОГНОЗ ИИ
# ==========================================

features = extract_features(password)
prediction = model.predict(features)[0]

if prediction == 0:
    level = "Слабый"
elif prediction == 1:
    level = "Средний"
else:
    level = "Сильный"

# ==========================================
# РЕКОМЕНДАЦИИ
# ==========================================

recommendations = []

if len(password) < 12:
    recommendations.append("увеличить длину до 12+ символов")

if not any(c.isupper() for c in password):
    recommendations.append("добавить заглавные буквы")

if not any(c.isdigit() for c in password):
    recommendations.append("добавить цифры")

if not any(not c.isalnum() for c in password):
    recommendations.append("добавить специальные символы")

# ==========================================
# ВЫВОД РЕЗУЛЬТАТА
# ==========================================

print("\n===== SECUREMIND =====")
print(f"Пароль: {password}")
print(f"Надежность: {score}%")
print(f"Оценка ИИ: {level}")

if recommendations:
    print("\nРекомендации:")
    for rec in recommendations:
        print("-", rec)
else:
    print("\nПароль соответствует всем основным требованиям безопасности.")

print("\nАнализ завершен.")