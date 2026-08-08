import os
import telebot

# استدعاء التوكن ومعرف القناة من متغيرات البيئة في Railway (أو وضعها مباشرة)
TOKEN = os.environ.get('BOT_TOKEN', 'ضع_توكن_البوت_هنا')
CHANNEL_ID = os.environ.get(
    'CHANNEL_ID', '@اسم_قناتك_أو_معرفها'
)  # مثال: '@reading_community'

bot = telebot.TeleBot(TOKEN)

# قاموس لتخزين الكتب المؤرشفة
CHANNEL_BOOKS = {}


# أرشفة المنشورات الجديدة القادمة من القناة تلقائياً
@bot.channel_post_handler(func=lambda message: True)
def archive_channel_posts(message):
  text_content = message.text or message.caption
  if text_content:
    # حفظ النص كاملًا بصيغة صغيرة للبحث المرن
    cleaned_text = text_content.strip().lower()
    CHANNEL_BOOKS[cleaned_text] = message.message_id

    # حفظ السطر الأول فقط كعنوان رئيسي أيضاً لسهولة المطابقة
    first_line = cleaned_text.split('\n')[0]
    CHANNEL_BOOKS[first_line] = message.message_id


# استقبال طلبات المستخدمين في المحادثة الخاصة
@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_private_requests(message):
  query = message.text.strip().lower()

  if query.startswith('/'):
    if query == '/start':
      bot.reply_to(
          message,
          'أهلاً بك في بوت مكتبة مجتمع القراءة 📚\nأرسل اسم الكتاب الذي تبحث عنه وسأقوم بإحضاره لك فوراً.',
      )
    return

  # البحث الذكي والفلترة ضمن الكتب المؤرشفة
  found_msg_id = None
  for title, msg_id in CHANNEL_BOOKS.items():
    if query in title:  # إذا كان الاسم المطللوب جزءاً من العنوان المؤرشف
      found_msg_id = msg_id
      break

  if found_msg_id:
    try:
      # إرسال أو توجيه الكتاب من القناة إلى الخاص
      bot.forward_message(
          chat_id=message.chat.id,
          from_chat_id=CHANNEL_ID,
          message_id=found_msg_id,
      )
    except Exception as e:
      bot.reply_to(
          message,
          f'❌ حدث خطأ أثناء محاولة جلب الكتاب تأكد من صلاحيات البوت في القناة.',
      )
  else:
    bot.reply_to(message, '❌ عذراً، لم أجد كتاباً بهذا الاسم في أرشيف القناة.')


if __name__ == '__main__':
  print('البوت يعمل الآن بنجاح...')
  bot.infinity_polling()
