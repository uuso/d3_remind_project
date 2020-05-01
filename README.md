Пробный проект "Библиотека"
----

В проекте пока что преимущественно бэкенд и самый примитивный фронт. На текущем этапе реализованы возможности: many2many отношения (несколько авторов у книг, выдача книг друзьям), страницы на базе Class based views, наследование шаблонов, раздача статических файлов, возможность привязать фотографии к объектам моделей Author и Book.

- Для работы потребуется указать переменную окружения **SECRET_KEY**.

#### Демонстрационная база данных:
Примените миграции, загрузите наиболее свежую фикстуру f$.xml. Вход в админку - *[one:one]*

##### Доступные наиболее интересные пути:
Путь| Назначение|
-|-
[*/*](http://he1.before.best/)                   |Наконец сделал редирект|
[*/common*](http://he1.before.best/common)|D7 - практика регистрации пользователей и работы с allauth/ Для работы потребуется создать в админке объект SocialApplications (проверено, работает)
[*/admin*](http://he1.before.best/admin)              |Админка, больше всего информации тут|
[*/index/*](http://he1.before.best/index/)              |Список книг|
[*/buddy/*](http://he1.before.best/buddy/)|Просмотр, удаление, редактирование друзей

В процессе разработки проект развернут на платформе Heroku: http://he1.before.best/