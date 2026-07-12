import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

api_key = os.getenv("OPENROUTER_API_KEY")
print(f"DEBUG: API Key length is {len(api_key) if api_key else 'NONE'}") # این خط رو اضافه کن

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

# تنظیم کلاینت OpenRouter
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام مهدی جان! من آماده تحلیل هستم.")

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # پیام «در حال فکر کردن» برای کاربر
    status_msg = await update.message.reply_text("درحال تحلیل...")
    
    try:
        # ارسال پیام به مدل
        completion = client.chat.completions.create(
          model="deepseek/deepseek-chat",
          messages=[{"role": "user", "content": user_text}]
        )
        answer = completion.choices[0].message.content
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=answer)
    except Exception as e:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=f"خطا در ارتباط با هوش مصنوعی: {str(e)}")

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("خطا: توکن بات یافت نشد!")
        exit(1)
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_ai))
    
    application.run_polling()
