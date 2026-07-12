a/Desktop\my-telegram-bot-v2\main.py → b/Desktop\my-telegram-bot-v2\main.py
@@ -1,41 +1,37 @@
 import os
+import logging
 from openai import OpenAI
 from telegram import Update
 from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
 
-# گرفتن کلید از محیط
-api_key = os.getenv("OPENROUTER_API_KEY")
+# تنظیم لاگ برای دیباگ کردن
+logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
 
-# لاگ برای دیباگ کردن متغیر محیطی
-print(f"DEBUG: API Key length is {len(api_key) if api_key else 'NONE'}")
-
-# تنظیم کلاینت OpenRouter
+# تنظیم کلاینت OpenRouter با مدل Gemini 1.5 Pro
 client = OpenAI(
   base_url="https://openrouter.ai/api/v1",
-  api_key=api_key,
-  default_headers={
-      "HTTP-Referer": "https://github.com/mahkh093/my-telegram-bot", # آدرس مخزن شما
-      "X-Title": "My Telegram Bot"
-  }
+  api_key=os.getenv("OPENROUTER_API_KEY"),
+  default_headers={"HTTP-Referer": "https://railway.app/", "X-Title": "EngineeringBot"}
 )
 
 async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
-    await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام مهدی جان! من آماده تحلیل هستم.")
+    await update.message.reply_text("سلام مهدی جان! من با هوشِ گوگل (Gemini 1.5 Pro) آماده تحلیل مهندسی هستم.")
 
 async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
     user_text = update.message.text
-    status_msg = await update.message.reply_text("درحال تحلیل...")
+    # نمایش پیام وضعیت برای درک بهتر کاربر
+    status_msg = await update.message.reply_text("درحال پردازش...")
     
     try:
-        # ارسال پیام به مدل
+        # استفاده از مدل Gemini 1.5 Pro
         completion = client.chat.completions.create(
-          model="deepseek/deepseek-chat",
+          model="google/gemini-pro-1.5", 
           messages=[{"role": "user", "content": user_text}]
         )
         answer = completion.choices[0].message.content
         await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=answer)
     except Exception as e:
-        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=f"خطا در ارتباط با هوش مصنوعی: {str(e)}")
+        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=f"خطای مدل: {str(e)}")
 
 if __name__ == '__main__':
     TOKEN = os.getenv("BOT_TOKEN")
@@ -48,4 +44,5 @@
     application.add_handler(CommandHandler('start', start))
     application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_ai))
     
+    # استفاده از run_polling برای اجرا
     application.run_polling()
