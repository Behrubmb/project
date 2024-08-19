from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler
from datetime import datetime, timedelta

TOKEN = '7377082003:AAEsPxDkIBfSNx6RJr3uJXcCmF6f-litsBE'

tasks = {}

def start(update, context):
    user_id = update.message.from_user.id
    if user_id not in tasks:
        tasks[user_id] = []
    message = ('Добро пожаловать в бот для контроля личных финансов!!\n'
               '\n\n Для получения информации введите /help')
    update.message.reply_text(message)

# Функция обработки команды /add
def add_transaction(update: Update, context: CallbackContext) -> None:
    # Инструкция для пользователя
    update.message.reply_text(
        "Введите данные о транзакции в формате:\n"
        "\"Сумма Категория Дата Описание\".\n"
        "Пример: \"500 Еда 2024-08-16 Обед в кафе\"."
    )
    
    # Установка состояния ожидания ответа
    return 'WAITING_FOR_TRANSACTION'

# Функция обработки сообщения с транзакцией
def handle_transaction(update: Update, context: CallbackContext) -> None:
    # Получаем сообщение от пользователя
    text = update.message.text
    try:
        # Разбиваем сообщение на части
        amount, category, date, description = text.split(' ', 3)
        
        # Формируем текст подтверждения
        confirmation_message = (
            f"Транзакция добавлена:\n"
            f"Сумма: {amount}\n"
            f"Категория: {category}\n"
            f"Дата: {date}\n"
            f"Описание: {description}"
        )
        
        # Отправляем подтверждение пользователю
        update.message.reply_text(confirmation_message)
        
    except ValueError:
        # Обрабатываем ошибку в случае неправильного формата ввода
        update.message.reply_text("Ошибка: Неправильный формат. Пожалуйста, используйте формат 'Сумма Категория Дата Описание'.")







# Пример данных транзакций (в реальном приложении данные будут храниться в базе данных)
transactions = [
    {"amount": 500, "category": "Еда", "date": "2024-08-16", "description": "Обед в кафе"},
    {"amount": 1000, "category": "Транспорт", "date": "2024-08-15", "description": "Такси"},
    {"amount": 2000, "category": "Развлечения", "date": "2024-08-10", "description": "Кино"}
]

# Функция для фильтрации транзакций по дате
def filter_transactions(period: str) -> list:
    now = datetime.now()
    if period == 'today':
        filtered = [t for t in transactions if t["date"] == now.strftime('%Y-%m-%d')]
    elif period == 'week':
        week_ago = now - timedelta(days=7)
        filtered = [t for t in transactions if datetime.strptime(t["date"], '%Y-%m-%d') >= week_ago]
    elif period == 'month':
        month_ago = now - timedelta(days=30)
        filtered = [t for t in transactions if datetime.strptime(t["date"], '%Y-%m-%d') >= month_ago]
    elif period == 'all_time':
        filtered = transactions
    return filtered

# Функция обработки команды /view
def view_transactions(update: Update, context: CallbackContext) -> None:
    # Создаем кнопки для выбора периода
    keyboard = [
        [
            InlineKeyboardButton("Сегодня", callback_data='today'),
            InlineKeyboardButton("Неделя", callback_data='week'),
        ],
        [
            InlineKeyboardButton("Месяц", callback_data='month'),
            InlineKeyboardButton("Всё время", callback_data='all_time'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Сообщение с выбором периода
    update.message.reply_text("Выберите период для просмотра транзакций:", reply_markup=reply_markup)

# Функция обработки выбора периода
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    period = query.data
    transactions_list = filter_transactions(period)
    
    if not transactions_list:
        response_text = "Транзакции не найдены."
    else:
        if period == 'today':
            response_text = "Транзакции за сегодня:\n"
        elif period == 'week':
            response_text = "Транзакции за последнюю неделю:\n"
        elif period == 'month':
            response_text = "Транзакции за последний месяц:\n"
        else:
            response_text = "Все транзакции:\n"
        
        # Формируем список транзакций
        for transaction in transactions_list:
            response_text += f"{transaction['amount']} {transaction['category']} {transaction['date']} {transaction['description']}\n"

    # Отправляем ответ пользователю
    query.edit_message_text(text=response_text)






# Функция для обработки команды /stats
def stats(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("По категориям", callback_data='category'),
            InlineKeyboardButton("По датам", callback_data='date'),
        ],
        [InlineKeyboardButton("Общий отчет", callback_data='summary')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите тип отчета:', reply_markup=reply_markup)

# Функция для обработки выбора пользователя
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Отчет по категориям
    if query.data == 'category':
        category_stats = "Расходы по категориям:\nЕда: 1000\nТранспорт: 500"
        query.edit_message_text(text=category_stats)

    # Отчет по датам
    elif query.data == 'date':
        date_stats = "Расходы по датам:\n2024-08-16: 500\n2024-08-15: 200"
        query.edit_message_text(text=date_stats)

    # Общий отчет
    elif query.data == 'summary':
        summary_stats = "Общие расходы:\nЗа месяц: 1500\nЗа год: 10000"
        query.edit_message_text(text=summary_stats)













# Функция обработки команды /settings
def settings(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Изменить валюту", callback_data='change_currency')],
        [InlineKeyboardButton("Установить напоминания", callback_data='set_reminders')],
        [InlineKeyboardButton("Сброс данных", callback_data='reset_data')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("Настройки:", reply_markup=reply_markup)

# Функция обработки выбора настроек
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'change_currency':
        # Подменю для выбора валюты
        currency_keyboard = [
            [InlineKeyboardButton("USD", callback_data='currency_usd')],
            [InlineKeyboardButton("EUR", callback_data='currency_eur')],
            [InlineKeyboardButton("RUB", callback_data='currency_rub')],
        ]
        reply_markup = InlineKeyboardMarkup(currency_keyboard)
        query.edit_message_text("Выберите валюту:", reply_markup=reply_markup)
    
    elif query.data == 'set_reminders':
        # Запрос на ввод времени для напоминаний
        query.edit_message_text("Введите время для напоминания о расходах (например, 18:00):")
        return 'WAITING_FOR_REMINDER_TIME'
    
    elif query.data == 'reset_data':
        # Подтверждение сброса данных
        reset_keyboard = [
            [InlineKeyboardButton("Да", callback_data='confirm_reset')],
            [InlineKeyboardButton("Нет", callback_data='cancel_reset')],
        ]
        reply_markup = InlineKeyboardMarkup(reset_keyboard)
        query.edit_message_text("Вы уверены, что хотите сбросить все данные? Это действие необратимо.", reply_markup=reply_markup)

# Функция обработки выбора валюты
def change_currency(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    currency = query.data.split('_')[1].upper()  # Получаем выбранную валюту
    query.edit_message_text(f"Валюта изменена на {currency}.")

# Функция обработки установки времени напоминания
def handle_reminder_time(update: Update, context: CallbackContext) -> None:
    time = update.message.text
    # В реальном приложении нужно добавить проверку формата времени и сохранить время напоминания
    update.message.reply_text(f"Напоминание установлено на {time}.")

# Функция обработки сброса данных
def reset_data(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'confirm_reset':
        # Здесь должен быть код для сброса всех данных
        query.edit_message_text("Все данные сброшены.")
    else:
        query.edit_message_text("Сброс данных отменён.")
    

def help(update, context):
    update.message.reply_text(
       "/start - Запуск бота.\n"
        "/add - Команда для доюовления новых транзакций.\n"
        "/view - Команда для просмотра всех записных транзакций.\n"
        "/stats - Команда для получения статистики по росходам.\n"
        "/settings - Команда для изменения настроек бота.\n"
        "/help - Показать список команд"
        )

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher


    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчик команды /add
    dispatcher.add_handler(CommandHandler("add", add_transaction))
    
    # Регистрируем обработчик текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_transaction))




        # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчик команды /view
    dispatcher.add_handler(CommandHandler("view", view_transactions))

    # Регистрируем обработчик нажатия кнопок
    dispatcher.add_handler(CallbackQueryHandler(button))


        # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчик команды /settings
    dispatcher.add_handler(CommandHandler("settings", settings))

    # Регистрируем обработчик нажатия кнопок
    dispatcher.add_handler(CallbackQueryHandler(button, pattern='^change_currency|set_reminders|reset_data$'))
    dispatcher.add_handler(CallbackQueryHandler(change_currency, pattern='^currency_'))
    dispatcher.add_handler(CallbackQueryHandler(reset_data, pattern='^confirm_reset|cancel_reset$'))

    # Регистрируем обработчик для ввода времени напоминания
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_reminder_time))





    updater.dispatcher.add_handler(CommandHandler("stats", stats))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))



    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add', add_transaction))
    dispatcher.add_handler(CallbackQueryHandler('view', view_transactions))
    
    dispatcher.add_handler(CallbackQueryHandler('settings', settings))
    dispatcher.add_handler(CommandHandler('help', help))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main() 





