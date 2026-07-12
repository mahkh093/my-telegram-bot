import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# تنظیمات لاگ‌گیری
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# اتصال به OpenRouter با فرمت رسمی که فرستادی
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
  default_headers={
      "HTTP-Referer": "https://github.com/mahkh093/my-telegram-bot",
      "X-Title": "EngineeringBot"
  }
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام مهدی جان! بات مهندسی با مدل DeepSeek V4 flash فعال است.")

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    status_msg = await update.message.reply_text("در حال پردازش...")

    try:
        # استفاده از مدل طبق مستندات رسمی
        completion = client.chat.completions.create(
          model="deepseek/deepseek-v4-flash",
          messages=[{"role": "user", "content": user_text}]
        )
        answer = completion.choices[0].message.content
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=answer)
    except Exception as e:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=f"خطا: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_ai))
    application.run_polling()
