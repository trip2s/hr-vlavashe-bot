from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re  # Для работы с регулярными выражениями

# ID группы, куда бот будет пересылать сообщения
GROUP_ID = -4614835180  # ID вашей группы

# Токен бота
API_TOKEN = "7382612863:AAESjEpO-NWmP1JbP5YSL-xFu1FXfsVwbkY"

# Функция для команды /start (реагирует только в личных сообщениях)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == 'private':  # Только в личных сообщениях
        await update.message.reply_text('Привіт! Я HR бот VLAVASHE.UA. Надішли своє резюме або повідомлення.')

# Обработка текстовых сообщений (с проверкой на номер телефона)
async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == 'private':  # Проверяем, что это личное сообщение
        user_message = update.message.text
        user_name = update.effective_user.first_name

        # Проверка, является ли сообщение номером телефона (от 10 до 12 цифр с допустимыми символами)
        if re.fullmatch(r'[+\d\s()]{10,20}', user_message) and sum(c.isdigit() for c in user_message) in range(10, 13):
            # Пересылаем сообщение в группу как номер телефона
            await context.bot.send_message(chat_id=GROUP_ID, text=f"Новий номер телефону від {user_name}: {user_message}")
            await update.message.reply_text('Дякуємо! Очікуйте дзвінка від адміністратора.')
        else:
            # Пересылаем сообщение в группу как обычное сообщение
            await context.bot.send_message(chat_id=GROUP_ID, text=f"Новое сообщение от {user_name}:\n{user_message}")
            await update.message.reply_text('Дякуємо за повідомлення! Не забудьте залишити свій телефон для зв’язку, ми зв’яжемося з вами найближчим часом.')

# Обработка резюме (файлов) только из личных сообщений
async def handle_private_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == 'private':  # Проверяем, что это личное сообщение
        document = update.message.document
        file_name = document.file_name
        user_name = update.effective_user.first_name
        # Сохраняем файл локально
        file = await document.get_file()
        file_path = f"./{file_name}"
        await file.download_to_drive(file_path)
        # Пересылаем файл в группу
        await context.bot.send_document(chat_id=GROUP_ID, document=open(file_path, 'rb'), caption=f"Новий файл від {user_name}: {file_name}")
        await update.message.reply_text('Дякуємо за ваше резюме! Не забудьте залишити свій телефон для зв’язку, ми зв’яжемося з вами найближчим часом.')

# Основная функция для запуска бота
def main():
    application = Application.builder().token(API_TOKEN).build()

    # Команда /start
    application.add_handler(CommandHandler('start', start))
    # Обработка текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_private_message))
    # Обработка файлов
    application.add_handler(MessageHandler(filters.Document.ALL, handle_private_document))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
