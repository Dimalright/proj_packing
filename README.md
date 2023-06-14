# proj_yandex
#
Откройте командную строку (терминал) и перейдите в каталог, где вы хотите развернуть проект.
#
git clone <https://github.com/Dimalright/proj_yandex.git>
#
Создайте вирутальное окружение командой py -m venv venv
#
Активируйте виртуальное окружение командой  source venv/Scripts/activate
#
Обновите pip install --upgrade pip
#
Далее установите зависимости с помощью pip install -r requirements.txt
#
Переходим в папку проекта cd packing_service
#
Прописываем команду py manage.py runserver
#
Документация будет доступна по адресу http://127.0.0.1:8000/api/v1/swagger/
#
Пример запроса апи: 
http://127.0.0.1:8000/api/v1/orders/d48f3211c1ffccdc374f23139a9ab668/
