# Microservice for Search Index of Phone Numbers

В рамках задачи были реализованы следующие задачи:

• нормализовать формат записи телефонных номеров, отсечь код страны, привести к формату удобному для поиска: "9291112233"

• результат сохранить в таблице - завести под неё новую колонку

• создать скрипт для запуска в фоновом режиме - ожидает новые телефонные номера, нормализует их, сохраняет в базу


# Как оно работает?

На базу данных production сервера накатывается миграция структуры БД, там же запускается скрипт синхронизации содержания двух колонок базы - с исходным и нормализованным номерами телефонов.

# Как использовать?

1. Создать копию базы данных, с помощью скрипта clone_db.py, предварительно добавив в ваши переменные среды SRC_DB_URI - URI исходной БД, FINAL_DB_URI - database URI создаваемой копии БД.
[Как это сделать в Windows?](http://ru.stackoverflow.com/questions/153628/%D0%9A%D0%B0%D0%BA-%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-%D0%B2-%D0%BF%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D1%83%D1%8E-%D0%BE%D0%BA%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-path-%D0%BF%D1%83%D1%82%D1%8C) [Linux?](http://ru.stackoverflow.com/questions/228/%D0%9A%D0%B0%D0%BA-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%B8%D1%82%D1%8C-%D0%BF%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D1%83%D1%8E-%D0%BE%D0%BA%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-linux-unix)

2. Миграция осуществляется средствами alembic, поэтому перед ее применением, необходимо в конфигурационном файле alembic.ini изменить параметр sqlalchemy.url, в который необходимо передать database uri вашей базы данных(FINAL_DB_URI).

Пример:

	sqlalchemy.url = postgresql://devman:devman@localhost/devman
	

Для запуска миграции выполнить следующую команду в терминале находясь в каталоге проекта:

	alembic upgrade head

3. Запуск скрипта нормализации format_phone.py, который заполнит созданную в предыдущем шаге колонку нормализованными телефонными номерами.


	python3 format_phone.py
	

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)