## Сайт Foodgram, «Продуктовый помощник». Техническое описание проекта

Сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать и скачивать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Сервисы и страницы проекта 

### Главная страница
Содержимое главной страницы — список первых шести рецептов, отсортированных по дате публикации (от новых к старым).  Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация.

### Страница рецепта
На странице — полное описание рецепта. Для авторизованных пользователей — возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта.

### Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.

### Подписка на авторов
Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.

Сценарий поведения пользователя:
1. Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
2. Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым)
3. При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».

### Список избранного
Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.

Сценарий поведения пользователя:
1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
2. Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
3. При необходимости пользователь может удалить рецепт из избранного.

### Список покупок
Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.

Сценарий поведения пользователя:

1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
2. Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
3. При необходимости пользователь может удалить рецепт из списка покупок.
Список покупок скачивается в формате .txt (или, по желанию, можно сделать выгрузку PDF).

При скачивании списка покупок ингредиенты в результирующем списке не должны дублироваться; если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке должен быть один пункт: Сахар — 15 г.

В результате список покупок может выглядеть так: <br>
> Фарш (баранина и говядина) (г) — 600 <br>
> Сыр плавленый (г) — 200 <br>
> Лук репчатый (г) — 50 <br>
> Картофель (г) — 1000 

### Фильтрация по тегам
При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов. 
При фильтрации на странице пользователя должны фильтроваться только рецепты выбранного пользователя. Такой же принцип должен соблюдаться при фильтрации списка избранного.

### Регистрация и авторизация
В проекте должна быть доступна система регистрации и авторизации пользователей. Чтобы собрать весь код для управления пользователями воедино — создайте приложение users. 

#### Обязательные поля для пользователя:
- Логин
- Пароль
- Email
- Имя
- Фамилия

#### Уровни доступа пользователей:
- Гость (неавторизованный пользователь)
- Авторизованный пользователь
- Администратор

#### Что могут делать неавторизованные пользователи
- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.

#### Что могут делать авторизованные пользователи
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингридиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

#### Что может делать администратор
Администратор обладает всеми правами авторизованного пользователя. 
Плюс к этому он может:
- изменять пароль любого пользователя,
- создавать/блокировать/удалять аккаунты пользователей,
- редактировать/удалять любые рецепты,
- добавлять/удалять/редактировать ингредиенты.
- добавлять/удалять/редактировать теги.
- Все эти функции нужно реализовать в стандартной админ-панели Django.

### Технические требования и инфраструктура
- Проект должен использовать базу данных PostgreSQL.
- Код должен находиться в репозитории foodgram-project-react.
- В Django-проекте должен быть файл requirements.txt со всеми зависимостями.
- Проект нужно запустить в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на вашем сервере в Яндекс.Облаке. Образ с проектом должен быть запушен на Docker Hub.
      
## Инструкции по развороту проекта 
### Для разворота проекта локально:

1) Установить и запустить [![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
2) Скачать данный репозиторий
3) В директории infra создать файл env. и наполнить его по образцу ниже:
  -  DB_NAME=postgres # имя базы данных
  -  POSTGRES_USER=postgres # логин для подключения к базе данных
  -  POSTGRES_PASSWORD=qwerty # пароль для подключения к БД (установите свой)
  -  DB_HOST=db # название сервиса (контейнера)
  -  DB_PORT=5432 # порт для подключения к БД
4) из директории infra/ выполнить команду 
``` docker compose up -d --build ```
5) после того как контейнеры nginx, db (БД PostgreSQL) и backend будут запущены, необходимо в контейнере backend создать и применить миграции, собрать статику, создать суперпользователя и загрузить данные с ингредиентами и тегами для создания рецептов. Для этого последовательно выполнить следующие команды:
 ```
    sudo docker-compose exec backend
    python manage.py migrate
    python manage.py collectstatic --no-input
    python manage.py createsuperuser
    python manage.py load_ingredienta_data
    python manage.py load_tags_data
 ``` 


### Для разворота проекта на удалённом сервере:

1) форкнуть данный репозитарий
2) в директориях backend и frontend находятся файлы Dockerfile. Необходимо собрать эти 2 образа и сохранить их на вашем репозитории DockerHub под соответствующими именами.
3) подготовьте сервер к деплою: необходимо установить docker, docker compose
5) в файле nginx.conf изменить server name на внешний ip вашего сервера.
6) скопировать файлы docker compose.yaml и nginx.conf и папку docs/ из проекта на сервер в домашнюю директорию
7) Добавьте в Secrets GitHub Actions переменные окружения для работы базы данных:
  -  DB_NAME=postgres # имя базы данных
  -  POSTGRES_USER=postgres # логин для подключения к базе данных
  -  POSTGRES_PASSWORD=qwerty # пароль для подключения к БД (установите свой)
  -  DB_HOST=db # название сервиса (контейнера)
  -  DB_PORT=5432 # порт для подключения к БД
  -  HOST=внешний IP сервера
  -  USER=имя пользователя для подключения к серверу
  -  SSH_KEY=приватный ключ с компьютера, имеющего доступ к боевому серверу
  -  PASSPHRASE=фраза-пароль ,если использовали её при создании ssh-ключа  
  -  DOCKER_USERNAME и DOCKER_PASSWORD - ваши логин и пароль на докерхаб.
    
6) выполните git push в ветку master, после чего будет запущен workflow: проверка кода flake8, обновление образа backend на вашем репозитории DockerHub и деплой на сервер
7) после успешного деплоя зайти на сервер и выполнить команды:
    ```
    sudo docker-compose exec backend
    python manage.py migrate
    python manage.py collectstatic --no-input
    python manage.py createsuperuser
    python manage.py load_ingredienta_data
    python manage.py load_tags_data
    ``` 

8) Теперь прект доступен по адресам:<br>

- Главная страница: http://<внешний IP сервера>/recipes/ <br>
- Докуметация к API: http://<внешний IP сервера>/api/docs/ <br>
- Админка: http://<внешний IP сервера>/admin/


Так же вы можете ознакомиться с функционалом на данный момент по адресу - http://taskipollot2.ddns.net
