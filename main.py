import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# تنظیم Google AI Studio
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

async def ask_ai(update: Update, context):
    user_text = update.message.text
    status_msg = await update.message.reply_text("درحال پردازش توسط هوش گوگل...")
    try:
        response = model.generate_content(user_text)
        await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                           message_id=status_msg.message_id,
                                           text=response.text)
    except Exception as e:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                           message_id=status_msg.message_id,
                                           text=f"خطا: {str(e)}")
# ... (بقیه کدهای start و main)
