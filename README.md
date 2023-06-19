Проект "proj_yandex"
Проект "proj_yandex" представляет собой систему, состоящую из двух сервисов: packing_service и ds_server. Эти сервисы предоставляют функциональность упаковки и обработки данных соответственно.

Установка
Убедитесь, что у вас установлен Docker и Docker Compose.
Склонируйте репозиторий проекта:
bash

git clone https://github.com/Dimalright/proj_yandex.git
Перейдите в корневую папку проекта:
bash

cd proj_yandex
Соберите и запустите контейнеры с помощью Docker Compose:
bash

docker-compose up
После успешного запуска контейнеров вы сможете получить доступ к сервисам:
packing_service будет доступен по адресу http://localhost:8000.
ds_server будет доступен по адресу http://localhost:8001.