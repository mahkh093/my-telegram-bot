import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.INFO)

# تنظیم کلاینت طبق داکیومنت OpenRouter
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
  default_headers={
      "HTTP-Referer": "https://railway.app/",
      "X-Title": "EngineeringBot"
  }
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! بات من با مدل Nemotron-3 Ultra 550B آماده تحلیل مهندسی است.")

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    status_msg = await update.message.reply_text("در حال پردازش با قدرت NVIDIA...")

    try:
        # نام مدل دقیقاً طبق مستندات سایت OpenRouter
        completion = client.chat.completions.create(
          model="nvidia/nemotron-3-ultra-550b-a55b:free",
          messages=[{"role": "user", "content": user_text}]
        )
        answer = completion.choices[0].message.content
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=answer)
    except Exception as e:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=f"خطا: {str(e)}")

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_ai))

    application.run_polling()
