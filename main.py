import os
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# کلاینت جدید گوگل
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

async def start(update: Update, context):
    await update.message.reply_text("سلام! بات من با مدل Gemini 2.0 (Google GenAI) آماده تحلیل است.")

async def ask_ai(update: Update, context):
    user_text = update.message.text
    status_msg = await update.message.reply_text("درحال پردازش توسط هوش گوگل...")

    try:
        # فراخوانی مدل جدید (gemini-2.0-flash برای سرعت و دقت بالا)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_text,
        )
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=status_msg.message_id,
            text=response.text
        )
    except Exception as e:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=status_msg.message_id,
            text=f"خطا در مدل گوگل: {str(e)}"
        )

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_ai))
    application.run_polling()
