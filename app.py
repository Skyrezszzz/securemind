import streamlit as st
from sklearn.ensemble import RandomForestClassifier

# =========================
# НАСТРОЙКА СТРАНИЦЫ
# =========================

st.set_page_config(page_title="SECUREMIND", page_icon="🔐", layout="centered")

st.title("🔐 SECUREMIND Password AI")
st.write("Анализ надежности пароля с ИИ и рекомендациями")

# =========================
# ФУНКЦИЯ ПРИЗНАКОВ
# =========================

def extract_features(password):
    return [[
        len(password),
        int(any(c.isupper() for c in password)),
        int(any(c.islower() for c in password)),
        int(any(c.isdigit() for c in password)),
        int(any(not c.isalnum() for c in password))
    ]]

# =========================
# ОБУЧЕНИЕ МОДЕЛИ
# =========================

passwords = [
    "123456", "password", "qwerty", "admin", "welcome",
    "Qwerty123", "Hello2024", "Abc123!",
    "Secure@2025", "X9#kLm2@Pq"
]

labels = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2]

X = []
for p in passwords:
    X.append([
        len(p),
        int(any(c.isupper() for c in p)),
        int(any(c.islower() for c in p)),
        int(any(c.isdigit() for c in p)),
        int(any(not c.isalnum() for c in p))
    ])

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, labels)

# =========================
# СЛАБЫЕ ПАРОЛИ
# =========================

weak_passwords = [
    "123456", "password", "qwerty", "admin", "welcome",
    "12345678", "000000"
]

# =========================
# ВВОД ПАРОЛЯ
# =========================

password = st.text_input("Введите пароль", type="password")

if password:

    # проверка базы
    if password.lower() in weak_passwords:
        st.warning("⚠ Пароль найден в базе слабых паролей!")

    # =========================
    # SCORE
    # =========================

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

    st.subheader("📊 Надежность")
    st.progress(score / 100)
    st.write(f"Score: {score}%")

    # =========================
    # ИИ ПРЕДСКАЗАНИЕ
    # =========================

    features = extract_features(password)
    prediction = model.predict(features)[0]

    if prediction == 0:
        st.error("🔴 Слабый пароль")
    elif prediction == 1:
        st.warning("🟠 Средний пароль")
    else:
        st.success("🟢 Сильный пароль")

    # =========================
    # РЕКОМЕНДАЦИИ
    # =========================

    st.subheader("💡 Рекомендации")

    recs = []

    if len(password) < 12:
        recs.append("Увеличить длину до 12+ символов")
    if not any(c.isupper() for c in password):
        recs.append("Добавить заглавные буквы")
    if not any(c.isdigit() for c in password):
        recs.append("Добавить цифры")
    if not any(not c.isalnum() for c in password):
        recs.append("Добавить спецсимволы")

    if recs:
        for r in recs:
            st.write("•", r)
    else:
        st.success("Пароль уже достаточно сильный")

st.divider()
st.caption("SECUREMIND • Password AI System")