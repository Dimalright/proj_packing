#"API" Проект "proj_yandex" представляет собой систему, состоящую из двух сервисов: packing_service и ds_server. Эти сервисы предоставляют функциональность упаковки и обработки данных соответственно.
#
Установка Убедитесь, что у вас установлен Docker и Docker Compose. Склонируйте репозиторий проекта: bash
#
git clone https://github.com/Dimalright/proj_yandex.git Перейдите в корневую папку проекта: bash
#
cd proj_yandex Соберите и запустите контейнеры с помощью Docker Compose: bash
#
docker-compose up
#
После успешного запуска контейнеров вы сможете получить доступ к сервисам:
packing_service будет доступен по адресу http://localhost:8000.
ds_server будет доступен по адресу http://localhost:8001.
#
Примеры запросов к API:
http://127.0.0.1:8000/api/v1/orders/
http://localhost:8000/api/v1/packaging/8772b0f4c363e4bc4945c999858951f9/
