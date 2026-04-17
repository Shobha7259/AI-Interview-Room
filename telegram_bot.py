import os
from dotenv import load_dotenv
from openai import OpenAI

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# AI FUNCTION
# -----------------------------
def get_ai_response(user_message):
    prompt = f"""
    You are an AI Interview Assistant.

    If user gives:
    - Question → generate answer
    - Answer → give feedback + score

    User input: {user_message}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -----------------------------
# TELEGRAM HANDLER
# -----------------------------
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print("User:", user_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_text}]
    )

    reply = response.choices[0].message.content

    await update.message.reply_text(reply)


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()