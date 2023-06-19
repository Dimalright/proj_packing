# Проект хакатона от Yandex Market. Команда № 4

Состав команды:
- Project Manager: @alexa_ch99
- Designer: @oneyasova, @great_but_not_gatsby
- Frontend developer: @dashall24, @t0pall
- Backend developer: @dimalright
- DS: @Sta9islaus @vododokhov21 @yaroslav_kn

- Бэкенд написан на Python при помощи библиотеке Django


Установка Убедитесь, что у вас установлен Docker и Docker Compose.
#
Склонируйте репозиторий проекта:
#
- git clone https://github.com/Dimalright/proj_yandex.git
#
Перейдите в корневую папку проекта: 
#
- cd proj_yandex
#
Соберите и запустите контейнеры с помощью Docker Compose: 
#
- docker-compose up
#
После успешного запуска контейнеров вы сможете получить доступ к сервисам:
#
packing_service будет доступен по адресу http://localhost:8000.
#
ds_server будет доступен по адресу http://localhost:8001.
#
Примеры запросов к API:
#
http://127.0.0.1:8000/api/v1/orders/
#
http://localhost:8000/api/v1/packaging/8772b0f4c363e4bc4945c999858951f9/
#
API-документация:
http://127.0.0.1:8000/api/v1/swagger/

