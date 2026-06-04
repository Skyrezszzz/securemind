```python
import streamlit as st
import pandas as pd
import numpy as np
import secrets
import string
from sklearn.ensemble import RandomForestClassifier

# ==================================
# НАСТРОЙКА СТРАНИЦЫ
# ==================================

st.set_page_config(
    page_title="SECUREMIND 2.0",
    page_icon="🔐",
    layout="wide"
)

# ==================================
# ОБУЧЕНИЕ МОДЕЛИ
# ==================================

def extract_features(password):
    return [
        len(password),
        int(any(c.isupper() for c in password)),
        int(any(c.islower() for c in password)),
        int(any(c.isdigit() for c in password)),
        int(any(not c.isalnum() for c in password))
    ]

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

labels = [0,0,0,0,0,1,1,1,2,2]

X = [extract_features(p) for p in passwords]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, labels)

weak_passwords = [
    "123456",
    "password",
    "qwerty",
    "admin",
    "welcome",
    "12345678",
    "000000"
]

# ==================================
# ГЕНЕРАТОР ПАРОЛЕЙ
# ==================================

def generate_password(length=16):

    chars = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*()_+-="
    )

    return ''.join(
        secrets.choice(chars)
        for _ in range(length)
    )

# ==================================
# AI ПОМОЩНИК
# ==================================

knowledge_base = {

    "пароль":
    """
Используйте пароль длиной не менее 12 символов.

Добавляйте:
• Заглавные буквы
• Строчные буквы
• Цифры
• Спецсимволы

Не используйте один пароль для нескольких сайтов.
""",

    "фишинг":
    """
Признаки фишинга:

• Срочность
• Угрозы блокировки
• Подозрительные ссылки
• Запрос паролей

Никогда не вводите пароль по ссылкам из сообщений.
""",

    "2fa":
    """
Двухфакторная аутентификация значительно повышает безопасность.

Рекомендуется включить её:
• Для почты
• Telegram
• Instagram
• Банковских сервисов
""",

    "вирус":
    """
Используйте антивирус.

Не скачивайте файлы с неизвестных сайтов.

Регулярно обновляйте систему.
""",

    "безопасность":
    """
Основы цифровой безопасности:

• Уникальные пароли
• 2FA
• Проверка ссылок
• Регулярные обновления
• Осторожность с вложениями
"""
}

# ==================================
# БОКОВОЕ МЕНЮ
# ==================================

st.sidebar.title("🔐 SECUREMIND")

page = st.sidebar.radio(
    "Выберите раздел",
    [
        "Главная",
        "Анализатор паролей",
        "Генератор паролей",
        "Оценка безопасности",
        "Детектор фишинга",
        "AI-помощник"
    ]
)

# ==================================
# ГЛАВНАЯ
# ==================================

if page == "Главная":

    st.title("🔐 SECUREMIND 2.0")

    st.subheader(
        "Интеллектуальная платформа кибербезопасности"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Модули", "5")
    col2.metric("ИИ-анализ", "Да")
    col3.metric("Защита", "Высокая")

    st.markdown("---")

    st.write("✅ Анализатор паролей")
    st.write("✅ Генератор паролей")
    st.write("✅ Оценка безопасности")
    st.write("✅ Детектор фишинга")
    st.write("✅ AI-помощник")

# ==================================
# АНАЛИЗАТОР ПАРОЛЕЙ
# ==================================

elif page == "Анализатор паролей":

    st.title("🔐 Анализатор паролей")

    password = st.text_input(
        "Введите пароль",
        type="password"
    )

    if password:

        if password.lower() in weak_passwords:
            st.error(
                "Пароль найден в базе слабых паролей"
            )

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

        st.progress(score / 100)

        st.metric(
            "Надёжность",
            f"{score}%"
        )

        prediction = model.predict(
            [extract_features(password)]
        )[0]

        if prediction == 0:
            st.error("Слабый пароль")

        elif prediction == 1:
            st.warning("Средний пароль")

        else:
            st.success("Сильный пароль")

        st.subheader("Рекомендации")

        recommendations = []

        if len(password) < 12:
            recommendations.append(
                "Увеличьте длину до 12 символов"
            )

        if not any(c.isupper() for c in password):
            recommendations.append(
                "Добавьте заглавные буквы"
            )

        if not any(c.isdigit() for c in password):
            recommendations.append(
                "Добавьте цифры"
            )

        if not any(not c.isalnum() for c in password):
            recommendations.append(
                "Добавьте спецсимволы"
            )

        if recommendations:
            for item in recommendations:
                st.write("•", item)
        else:
            st.success(
                "Пароль соответствует требованиям"
            )

# ==================================
# ГЕНЕРАТОР ПАРОЛЕЙ
# ==================================

elif page == "Генератор паролей":

    st.title("🔑 Генератор паролей")

    length = st.slider(
        "Длина пароля",
        8,
        32,
        16
    )

    if st.button("Сгенерировать"):

        password = generate_password(length)

        st.code(password)

        st.success(
            "Пароль успешно создан"
        )

# ==================================
# ОЦЕНКА БЕЗОПАСНОСТИ
# ==================================

elif page == "Оценка безопасности":

    st.title("🛡 Оценка безопасности")

    same = st.radio(
        "Используете одинаковые пароли?",
        ["Да", "Нет"]
    )

    twofa = st.radio(
        "Включена 2FA?",
        ["Да", "Нет"]
    )

    manager = st.radio(
        "Используете менеджер паролей?",
        ["Да", "Нет"]
    )

    wifi = st.radio(
        "Часто используете публичный Wi-Fi?",
        ["Да", "Нет"]
    )

    if st.button("Рассчитать"):

        score = 100

        if same == "Да":
            score -= 30

        if twofa == "Нет":
            score -= 30

        if manager == "Нет":
            score -= 20

        if wifi == "Да":
            score -= 20

        score = max(score, 0)

        st.metric(
            "Индекс безопасности",
            f"{score}/100"
        )

        if score >= 80:
            st.success(
                "Высокий уровень защиты"
            )

        elif score >= 50:
            st.warning(
                "Средний уровень защиты"
            )

        else:
            st.error(
                "Низкий уровень защиты"
            )

# ==================================
# ДЕТЕКТОР ФИШИНГА
# ==================================

elif page == "Детектор фишинга":

    st.title("🚨 Детектор фишинга")

    text = st.text_area(
        "Вставьте сообщение"
    )

    if st.button("Проверить сообщение"):

        danger_words = [
            "срочно",
            "аккаунт",
            "заблокирован",
            "пароль",
            "перейдите",
            "выиграли",
            "подтвердите",
            "банк",
            "карта"
        ]

        risk = 0

        for word in danger_words:

            if word in text.lower():
                risk += 12

        risk = min(risk, 100)

        st.progress(risk / 100)

        st.metric(
            "Риск фишинга",
            f"{risk}%"
        )

        if risk >= 60:
            st.error(
                "Высокая вероятность фишинга"
            )

        elif risk >= 30:
            st.warning(
                "Подозрительное сообщение"
            )

        else:
            st.success(
                "Явных признаков фишинга не найдено"
            )

# ==================================
# AI ПОМОЩНИК
# ==================================

elif page == "AI-помощник":

    st.title("🤖 AI-помощник")

    question = st.text_input(
        "Задайте вопрос"
    )

    if question:

        question = question.lower()

        found = False

        for key, answer in knowledge_base.items():

            if key in question:

                st.success(answer)

                found = True

                break

        if not found:

            st.info(
                """
Я пока не знаю ответа на этот вопрос.

Попробуйте спросить про:
• пароль
• фишинг
• 2FA
• вирусы
• безопасность
"""
            )

st.markdown("---")
st.caption(
    "SECUREMIND 2.0 • AI Cyber Security Platform"
)
