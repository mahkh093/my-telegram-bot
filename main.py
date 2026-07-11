import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# تنظیمات لاگ برای دیباگ کردن
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# تابع شروع بات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام مهدی جان! بات من فعاله.")

if __name__ == '__main__':
    # گرفتن توکن از متغیر محیطی (Railway از اینجا می‌خونه)
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        print("خطا: توکن بات یافت نشد!")
        exit(1)
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()
