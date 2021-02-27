# REST API для списка произведений YaMDb
<!---
https://github.com/cement-hools/yamdb_final/workflows/yamdbworkflow/badge.svg
--->
![yamdb%20workflow Actions Status](https://github.com/cement-hools/yamdb_final/workflows/yamdb%20workflow/badge.svg)

Выводит список произведений, сортировка по групам и жанрам. Возможность оставить отзыв и рейтинг. Коментарии к отзывам. <br> Реализована регистрация с отправкой токкена на email


### Установка
- склонируйте проект с реппозитория GitHub
    ```
    git clone https://github.com/cement-hools/infra_sp2
    ```
- перейдите в директорию infra_sp2
    ```
    cd infra_sp2
    ```
- запустите docker-compose
    ```
    docker-compose up
    ```
 - выполните миграции
    ```
    docker-compose exec web python manage.py migrate
    ```   
 - создать суперпользователя
    ```
    docker-compose exec web python manage.py createsuperuser
    ```  
    Введите username, email, password<br><br>
 - заполнить базу тестовыми данными (если требуется)
    ```
    docker-compose exec web python manage.py loaddata fixtures.json
    ```  

### Документация по использованию
- после установки перейдите в браузре на http://localhost:8000/redoc/ 

### Проект развернут по адресу
- http://130.193.43.51:8000/redoc/