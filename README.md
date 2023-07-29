# test_task_for_Bottec
Тестовое задание для компании Bottec (телеграм бот + админ панель джанго).

## Описание проекта:
Код реализует работу телеграм бота для покупок товара.

У бота есть три раздела:
- Каталог
- Корзина
- FAQ

## Каталог
- в каталоге реализовано меню из inline кнопок для выбора категорий и подкатегорий товаров;
- отправляются пользователю все товары выбранной подкатегории (один товар - одно сообщение)
  - под каждым товаром есть inline кнопка - Добавить в корзину
  - отправляется фся информация о товаре (фото, описание, цена);
- товар можно добавить в корзину с указанием его количества (под каждым товаром есть inline кнопка - Добавить в корзину)
- после покупки товара пользователь автоматически переходит в корзину.

## Корзина
- Просмотр информации о товарах в корзине (название, количество, общая стоимость);
- Удаление товара из корзины (через inline кнопки);
- Оформление заказа
  - ввод адреса (просто текст - пока не проверяется);
  - оплата через YMoney
    - оплата тестова - ограничение с 60 до 1000 рублей
    - тестовая карта - № 1111 1111 1111 1026, срок: 12/26, код:000

## FAQ
- Ответы на частозадаваемые вопросы в формате inline режима с автоматическим дополнением вопроса

Созданы модели:

- Профилей пользователей
- Категорий
- Подкатегорий
- Товаров
- Заказов
- Позиции заказа
- Рассылки

Особенности:
- Админ панель на Django (управление БД);
- Установлена связь телеграмм бота и Django (через модели для работы с БД);
- После запуска бот проверяет подписку на канал и группу в телеграмме;
- Категории и подкатегории товаров реализуются в формате inline кнопок;
- Все успешно оплаченные заказы записываются в эксель таблицу


## Запуск проекта
1) Склонируйте репозиторий.

2) Добавьте и заполните ```.env``` файл

3) Запустите проект

    Запустить проект можно командой:
    
    ```
    docker-compose up
    ```
    
    Утановите разрешенный IP (IP вашего сервера) для админ панели. В папке admin_panel ➡️ admin_panel ➡️ settings.py
    
    ```
    ALLOWED_HOSTS = ['<IP вашего сервера>', '127.0.0.1', 'localhost']
    ```
    
    После команды docker-compose up. Перейдите в контейнер admin_panel
    ```
    docker exec -it admin_panel bash
    ```
    
    И пропишите команду для создания супер пользователя:
    ```
    python manage.py createsuperuser
    ```
    
    Все миграции выполняются автоматически.

4) Заполните базу данных (категории, подкатегории, товары) через админ меню.

