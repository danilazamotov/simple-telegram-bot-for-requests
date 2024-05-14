# telegram-bot-for-requests
Telegram bot for generating customer requests, based on sqllite+aiogram

Steps:
1. Transfer the received files to a location convenient for you.
2. Log in to telegram on behalf of the director and accountant, telegram bot (https://t.me/getmyid_bot)
and send him any of your messages from other groups (Remember your user ID:) FOR the director and accountant!
3. Go to the Telegram bot https://t.me/BotFather and create a new bot, name it as you wish, remember its API token.
4. Open the .env file using notepad and paste the values into the file, saving (TELEGRAM_BOT_API_KEY=token API
(you can use my token, but this does not guarantee further functionality, DIRECTOR_ID=director, ACCOUNTING_ID=accountant).
5. Next, run start .exe or .bat
6. Use Telegram bot!
7. To continue using it, you can close the console.

Шаги:
1. Загрузите полученные файлы в удобное для вас место.
2. Зайдите в телеграмм от имени директора и бухгалтера, телеграм-бот (https://t.me/getmyid_bot) 
		и отправьте ему любое ваше сообщение из других групп (Запомните ваш ID пользователя:) ДЛЯ директора и бухгалтера!
3. Зайдите в бот Telegram https://t.me/BotFather и создайте нового бота, назовите его по вашему желанию, запомните его API-токен.
4. Откройте файл .env с помощью блокнота и вставьте значения в файл, сохраните (TELEGRAM_BOT_API_KEY=токен API 
		(вы можете использовать мой токен, но не гарантируется дальнейшая работоспособность, DIRECTOR_ID=директор, ACCOUNTING_ID=бухгалтер).
5. Далее запускаем .exe или .bat
6. Используйте Telegram-бот!
7. Чтобы завершить использование - вы можете закрыть консоль.

-------------------------------------------------------------
ДЛЯ СИСТЕМНОГО АДМИНИСТРАТОРА - добавить .bat файл в автозапуск системы, и опционально - выполнять резервное копирование БД по адресу database/requests.db
-------------------------------------------------------------

В режиме Директор или Бухгалтер имеется кнопка Статистика - она добавляет на экран те заявки, который вы потеряли или не подтвердили вовремя.
P.S.: В случае, если запуска не происходит, Установите https://www.python.org/downloads/release/python-3913/ или установите его из папки.
