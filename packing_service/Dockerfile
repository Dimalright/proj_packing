FROM python:3.10.9
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app/packing_service
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
