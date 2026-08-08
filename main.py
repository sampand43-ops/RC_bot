import telebot
import os

# استخدام التوكن الخاص بك
BOT_TOKEN = "8619586974:AAE9iQg0BBfswqIgBH5do4XSm2HqiiZQWIk"
CHANNEL_ID = -1004395670008  # معرف قناتك

bot = telebot.TeleBot(BOT_TOKEN)
CHANNEL_BOOKS = {}

# 1. أرشفة الكتب تلقائياً من القناة
@bot.channel_post_handler(func=lambda message: message.chat.id == CHANNEL_ID)
def save_books_from_channel(message):
    text_content = message.text or message.caption
    if text_content:
        book_title = text_content.split('\n')[0].strip().lower()
        CHANNEL_BOOKS[book_title] = message.message_id
        print(f"تم أرشفة كتاب: {book_title}")

# 2. الاستجابة لطلبات المستخدمين في الخاص
@bot.message_handler(func=lambda message: message.chat.type == "private")
def handle_private_requests(message):
    user_text = message.text.strip() if message.text else ""
    
    if user_text.startswith("اريد") or user_text.startswith("أريد"):
        target_book = user_text.replace("اريد", "").replace("أريد", "").strip().lower()
        
        if not target_book:
            bot.reply_to(message, "❌ الرجاء كتابة اسم الكتاب بعد كلمة (اريد).")
            return
            
        found_msg_id = None
        for title, msg_id in CHANNEL_BOOKS.items():
            if target_book in title:
                found_msg_id = msg_id
                break
                
        if found_msg_id:
            try:
                bot.forward_message(chat_id=message.chat.id, from_chat_id=CHANNEL_ID, message_id=found_msg_id)
                bot.reply_to(message, "✅ تفضل، تم إرسال الكتاب إليك مباشرة!")
            except Exception as e:
                bot.reply_to(message, f"⚠️ حدث خطأ أثناء التحويل: تأكد أن البوت مشرف في القناة.")
        else:
            bot.reply_to(message, "❌ عذراً، لم أجد كتاباً بهذا الاسم في أرشيف القناة.")
    else:
        bot.reply_to(message, "مرحباً بك في مكتبة مجتمع القراءة! أرسل لي صيغة (اريد [اسم الكتاب]) لطلب الكتاب فوراً.")

print("Bot is starting on Railway...")
bot.infinity_polling(skip_pending=True)