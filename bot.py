import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")

SYSTEM_PROMPT = """Ты помощник для учёта продаж команды. 
Ты помогаешь считать сколько каждый менеджер продал товаров, 
вести статистику, сравнивать показатели и делать отчёты.
Отвечай на русском языке."""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
        json={
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{user_name}: {user_message}"}
            ]
        }
    )
    
    reply = response.json()["choices"][0]["message"]["content"]
    await update.message.reply_text(reply)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
