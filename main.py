import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.INFO)

# چک کردن مستقیم کلید
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("CRITICAL ERROR: OPENROUTER_API_KEY is NOT set in environment variables!")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
  default_headers={"HTTP-Referer": "https://railway.app/", "X-Title": "EngineeringBot"}
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من با Gemini 1.5 Pro آماده‌ام.")

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not os.getenv("OPENROUTER_API_KEY"):
        await update.message.reply_text("خطا: کلید OpenRouter در سرور ست نشده است!")
        return

    status_msg = await update.message.reply_text("درحال پردازش...")
    try:
        completion = client.chat.completions.create(
          model="google/gemini-pro-1.5",
          messages=[{"role": "user", "content": user_text}]
        )
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=completion.choices[0].message.content)
    except Exception as e:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=f"خطا: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_ai))
    application.run_polling()
