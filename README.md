Пробный проект "Библиотека"
----

В проекте пока что преимущественно бэкенд и самый примитивный фронт.

- Для работы потребуется указать переменную окружения **SECRET_KEY**.

#### Демонстрационная база данных:
Примените миграции, загрузите фикстуру f4.xml. Вход в админку - *[one:one]*

##### Доступные пути:
Путь                  | Назначение|
-|-
*/*                   |Список названий книг|
*/admin*              |Админка, больше всего информации тут|
*/index*              |Список книг детально|
*/author*             |Тупо список авторов|
*/author/create*      |Добавить нового автора в БД|
*/author/createmany*  |Привязать авторов к книгам (используется many-to-many таблица)|