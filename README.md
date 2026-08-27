# AI Session Service

Мінімальний backend-сервіс для ведення чат-сесій з моделями OpenAI та розрахунку вартості використання токенів.

## Модель та тарифи
За замовчуванням використовується модель `gpt-4o-mini`. 
Розрахунок вартості базується на офіційних публічних тарифах OpenAI:
- Input tokens: $0.150 / 1M tokens ($0.00015 / 1k)
- Output tokens: $0.600 / 1M tokens ($0.00060 / 1k)

## Інструкція запуску
1. Встановіть залежності: `pip install -r requirements.txt`
2. Створіть файл `.env` на основі `.env.example` та вкажіть ваш `OPENAI_API_KEY`.
3. Запустіть сервер: `uvicorn main:app --reload`
База даних (SQLite) створиться автоматично при першому запуску. Документація API доступна за адресою `http://127.0.0.1:8000/docs`.

## Приклади API requests (cURL)

**1. Створити нову chat session (із заданням системного промпту):**
curl -X 'POST' \
  '[http://127.0.0.1:8000/api/v1/sessions](http://127.0.0.1:8000/api/v1/sessions)' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
  "model_name": "gpt-4o-mini",
  "system_prompt": "Ти досвідчений AI Engineer. Відповідай коротко."
}'

**2. Створити нову chat session:**
curl -X 'POST' \
  '[http://127.0.0.1:8000/api/v1/sessions](http://127.0.0.1:8000/api/v1/sessions)' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"model_name": "gpt-4o-mini"}'

**3. Надіслати повідомлення у конкретну session:**
(замініть {id} на UUID отриманої сесії)
curl -X 'POST' \
  '[http://127.0.0.1:8000/api/v1/sessions/](http://127.0.0.1:8000/api/v1/sessions/){id}/messages' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"content": "Привіт! Яка столиця України?"}'

**4. Отримати session, повну історію та накопичену вартість:**
curl -X 'GET' \
  '[http://127.0.0.1:8000/api/v1/sessions/](http://127.0.0.1:8000/api/v1/sessions/){id}' \
  -H 'Accept: application/json'



# Відомі обмеження
Архітектура: Для пришвидшення розробки та дотримання ліміту часу (MVP), бізнес-логіка не виносилася в глибокий шар окремих сервісів, а частково реалізована безпосередньо в маршрутизаторах (api/routes.py).

Управління контекстом: Не реалізовано механізм обрізання чи сумаризації контексту. Якщо історія повідомлень перевищить контекстне вікно моделі, буде повернуто помилку від OpenAI API.

Синхронність: Сервіс працює виключно синхронно, потокова передача даних не реалізовувалася.
