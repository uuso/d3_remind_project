Пробный проект "Библиотека"
----

В проекте пока что преимущественно бэкенд и самый примитивный фронт. На текущем этапе реализованы возможности: many2many отношения (несколько авторов у книг, выдача книг друзьям), страницы на базе Class based views, наследование шаблонов, раздача статических файлов, возможность привязать фотографии к объектам моделей Author и Book.

- Для работы потребуется указать переменную окружения **SECRET_KEY**.

#### Демонстрационная база данных:
Примените миграции, загрузите наиболее свежую фикстуру f$.xml. Вход в админку - *[one:one]*

##### Доступные наиболее интересные пути:
Путь                  | Назначение|
-|-
*/*                   |Наконец сделал редирект|
*/admin*              |Админка, больше всего информации тут|
*/index*              |Список книг|
*/buddy*|Просмотр, удаление, редактирование друзей

В процессе разработки проект развернут на платформе Heroku: http://he1.before.best/