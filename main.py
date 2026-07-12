import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
  default_headers={"HTTP-Referer": "https://railway.app/", "X-Title": "EngineeringBot"}
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام مهدی جان! من با هوشِ گوگل (Gemini 1.5 Pro) آماده تحلیل مهندسی هستم.")

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    status_msg = await update.message.reply_text("درحال پردازش...")

    try:
        completion = client.chat.completions.create(
          model="google/gemini-pro-1.5",
          messages=[{"role": "user", "content": user_text}]
        )
        answer = completion.choices[0].message.content
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=answer)
    except Exception as e:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=f"خطای مدل: {str(e)}")

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("خطا: توکن بات یافت نشد!")
        exit(1)

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_ai))
    application.run_polling()
