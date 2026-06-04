
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

# Текст подсказки, если совпадений не найдено
TOPICS_HINT = """
Извините, я пока не знаю ответа на этот вопрос. 
Попробуйте спросить про: **пароль**, **фишинг**, **2fa**, **вирус** или **безопасность**.
"""

def find_best_answer(user_input):
    """
    Ищет ключевые слова из базы знаний в вопросе пользователя.
    """
    input_lower = user_input.lower()
    for key, value in knowledge_base.items():
        if key in input_lower:
            return value
    return None


# ==================================
# ВЕРОЯТНОСТЬ ВЗЛОМА ПАРОЛЯ
# ==================================

def crack_probability(password):
    """
    Рассчитывает примерное время взлома пароля
    методом перебора (brute-force) и возвращает
    вероятность взлома в процентах (100 = очень легко,
    ~0 = практически невозможно).
    """
    import math

    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(not c.isalnum() for c in password):
        charset += 32
    if charset == 0:
        charset = 26

    length = len(password)
    combinations = charset ** length

    # Скорость перебора: ~10 млрд попыток/сек (современный GPU)
    guesses_per_second = 10_000_000_000
    seconds = combinations / guesses_per_second

    # Читаемое время взлома
    if seconds < 1:
        time_str = "менее секунды"
    elif seconds < 60:
        time_str = f"{int(seconds)} сек."
    elif seconds < 3600:
        time_str = f"{int(seconds // 60)} мин."
    elif seconds < 86400:
        time_str = f"{int(seconds // 3600)} ч."
    elif seconds < 31536000:
        time_str = f"{int(seconds // 86400)} дней"
    elif seconds < 3.154e10:
        time_str = f"{int(seconds // 31536000)} лет"
    elif seconds < 3.154e13:
        time_str = f"{int(seconds // 3.154e10)} тыс. лет"
    elif seconds < 3.154e16:
        time_str = f"{int(seconds // 3.154e13)} млн. лет"
    else:
        time_str = "практически невозможно"

    # Вероятность взлома по логарифмической шкале
    if seconds <= 0:
        probability = 100.0
    else:
        log_s = math.log10(max(seconds, 1))
        max_log = math.log10(3.154e16)
        probability = max(1.0, 100.0 - (log_s / max_log) * 99.0)

    return round(probability, 1), time_str


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

        # ---- Вероятность взлома ----
        st.subheader("💀 Вероятность взлома")

        prob, time_str = crack_probability(password)

        st.progress(prob / 100)

        col_a, col_b = st.columns(2)

        col_a.metric(
            "Вероятность взлома",
            f"{prob}%"
        )

        col_b.metric(
            "Время взлома (brute-force)",
            time_str
        )

        if prob >= 70:
            st.error(
                "⚠️ Пароль легко взломать методом перебора!"
            )
        elif prob >= 35:
            st.warning(
                "🔶 Пароль может быть взломан при наличии ресурсов."
            )
        else:
            st.success(
                "✅ Пароль устойчив к brute-force атаке."
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

    st.title("🤖 AI-помощник по кибербезопасности")

    st.markdown(
        "Задайте любой вопрос по кибербезопасности — пароли, фишинг, "
        "вирусы, VPN, шифрование, утечки данных и многое другое."
    )

    # Инициализация истории чата
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Отображение истории чата
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    # Поле ввода
    user_input = st.chat_input("Введите вопрос по кибербезопасности...")

    if user_input:

        # Сохраняем вопрос
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):

            answer = find_best_answer(user_input)

            if answer:
                st.markdown(answer)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })
            else:
                st.markdown(TOPICS_HINT)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": TOPICS_HINT
                })

    # Кнопка очистки
    if st.session_state.chat_history:
        st.markdown("---")
        if st.button("🗑️ Очистить историю чата"):
            st.session_state.chat_history = []
            st.rerun()

    # Подсказки
    st.markdown("---")
    st.markdown("**💡 Примеры вопросов:**")

    col1, col2, col3 = st.columns(3)

    col1.info("🔑 Как создать надёжный пароль?")
    col1.info("🗄️ Что такое менеджер паролей?")
    col1.info("💾 Что такое резервная копия?")

    col2.info("🎣 Как распознать фишинг?")
    col2.info("🛡️ Что такое двухфакторная аутентификация?")
    col2.info("📶 Безопасен ли публичный Wi-Fi?")

    col3.info("🦠 Что такое ransomware?")
    col3.info("🌐 Зачем нужен VPN?")
    col3.info("🔒 Как зашифровать диск?")

st.markdown("---")
st.caption(
    "SECUREMIND 2.0 • AI Cyber Security Platform"
)