import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Используем переменную окружения

KEYWORDS = [
    "пришлю за спасибо",
    "вышлю в лс",
    "напиши в лс",
    "дам бесплатно",
    "получи курс",
    "пришлю материалы",
    "недавно прочитал книгу",
    "вышлю чек-лист",
    "скачать гайд",
    "напиши плюсик",
    "напиши +",
    "забирай подарок",
    "ссылка в лс",
    "перешлю материал",
    "пришлю бесплатно",
    "недавно прошёл курс",
    "пришлю курс",
    "вышлю гайд",
    "ссылка на материалы",
    "отдам курс"
]

def normalize_text(text):
    substitutions = {
        "a": "а", "e": "е", "o": "о", "c": "с", "p": "р", "y": "у", "x": "х", "b": "в", "h": "н", "k": "к", "m": "м", "t": "т",
        "A": "А", "B": "В", "C": "С", "E": "Е", "H": "Н", "K": "К", "M": "М", "O": "О", "P": "Р", "T": "Т", "X": "Х", "Y": "У"
    }
    for latin, cyrillic in substitutions.items():
        text = text.replace(latin, cyrillic)
    return text.lower()

def contains_spam(text):
    normalized = normalize_text(text)
    for kw in KEYWORDS:
        if kw in normalized:
            return True
    return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        if contains_spam(update.message.text):
            try:
                await update.message.delete()
            except Exception as e:
                print(f"Ошибка при удалении: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Бот запущен...")
    app.run_polling()  # ВАЖНО: без await, без asyncio.run
