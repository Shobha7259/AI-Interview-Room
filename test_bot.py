import os
from dotenv import load_dotenv
from openai import OpenAI

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load env
load_dotenv()

TELEGRAM_TOKEN = "8704706604:AAFVNe_Hieue2Ixj4TqkNWoC1GKhRWg5FhA"

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Interview Bot"
    }
)

# Store user state
user_data = {}

# 🎯 Start Interview
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    user_data[user_id] = {
        "step": 0,
        "score": 0
    }

    await update.message.reply_text(
        "👋 Welcome to AI Interview Bot!\n\nFirst Question:\n👉 Tell me about yourself."
    )

# 🤖 AI evaluation
def evaluate_answer(answer):
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an interviewer. Give score out of 10 and short feedback."},
                {"role": "user", "content": answer}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("ERROR:", e)
        return "⚠️ Evaluation failed"

# 📩 Handle answers
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_text = update.message.text

    if user_id not in user_data:
        await update.message.reply_text("Type /start to begin interview")
        return

    step = user_data[user_id]["step"]

    # Evaluate answer
    feedback = evaluate_answer(user_text)
    await update.message.reply_text(f"📝 Feedback:\n{feedback}")

    # Next questions
    questions = [
        "👉 What are your strengths?",
        "👉 Why should we hire you?",
        "👉 Where do you see yourself in 5 years?"
    ]

    if step < len(questions):
        await update.message.reply_text(f"Next Question:\n{questions[step]}")
        user_data[user_id]["step"] += 1
    else:
        await update.message.reply_text("✅ Interview Completed! Good job 🎉")
        del user_data[user_id]

# 🚀 Main
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()