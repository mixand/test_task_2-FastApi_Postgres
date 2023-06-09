## test task 2

### Task:

Необходимо реализовать веб-сервис, выполняющий следующие функции:

1. Создание пользователя;
1. Для каждого пользователя - сохранение аудиозаписи в формате wav, преобразование её в формат mp3 и запись в базу
   данных и предоставление ссылки для скачивания аудиозаписи.

Детализация задачи:

1. С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно -
   PostgreSQL). Предоставить все необходимые скрипты и конфигурационные (docker/compose) файлы для развертывания СУБД, а
   также инструкции для подключения к ней. Необходимо обеспечить сохранность данных при рестарте контейнера (то есть -
   использовать volume-ы для хранения файлов СУБД на хост-машине.
1. Реализовать веб-сервис со следующими REST методами:
   1. Создание пользователя, POST:
      1. Принимает на вход запросы с именем пользователя;
      1. Создаёт в базе данных пользователя заданным именем, так же генерирует уникальный идентификатор пользователя и
         UUID токен доступа (в виде строки) для данного пользователя;
      1. Возвращает сгенерированные идентификатор пользователя и токен.
   1. Добавление аудиозаписи, POST:
      1. Принимает на вход запросы, содержащие уникальный идентификатор пользователя, токен доступа и аудиозапись в
         формате wav;
      1. Преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет их в базе
         данных;
      1. Возвращает URL для скачивания записи вида http://host:port/record?id=id_записи&user=id_пользователя.
   1. Доступ к аудиозаписи, GET:
      1. Предоставляет возможность скачать аудиозапись по ссылке из п 2.2.3.
1. Для всех сервисов метода должна быть предусмотрена предусмотрена обработка различных ошибок, возникающих при
   выполнении запроса, с возвращением соответствующего HTTP статуса.
1. Модель данных (таблицы, поля) для каждого из заданий можно выбрать по своему усмотрению.
1. В репозитории с заданием должны быть предоставлены инструкции по сборке докер-образа с сервисами из пп. 2. и 3., их
   настройке и запуску. А также пример запросов к методам сервиса.
1. Желательно, если при выполнении задания вы будете использовать docker-compose, SQLAlchemy, пользоваться аннотацией
   типов.

### Launch Instructions for Linux:
All settings are in the [.env](./.env) file.

In the terminal panel, run the following commands:

```
$ mkdir dbdata static && sudo docker-compose up --build
```

Examples of queries in the postman collection [test_2.postman_collection.json](./test_2.postman_collection.json).