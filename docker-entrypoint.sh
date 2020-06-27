#!/bin/bash

echo "======Собираем статику======"
if [ "$DEBUG" == "False" ]; then
    echo "======Загружаем в S3 облако, это займет некоторое время======"
fi
python manage.py collectstatic --noinput

echo "======Накатываем миграции======"
python manage.py makemigrations
python manage.py migrate


echo "======Стартуем сервер======"
if [ "$DEBUG" == "True" ]; then
    ./manage.py runserver 0.0.0.0:80
else


    daphne -e ssl:443:privateKey=config/ssl_keys/privkey.pem:certKey=config/ssl_keys/fullchain.pem  -b 0.0.0.0 -p 80 englishtalk.asgi:application

fi
