<a name="readme-top"></a>

<h3 align="center">Bewise test 2</h3>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">О проекте</a>
      <ul>
        <li><a href="#built-with">Технологии</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Подкотовка и запуск</a>
      <ul>
        <li><a href="#prerequisites">Предварительные условия</a></li>
        <li><a href="#installation">Как запустить</a></li>
      </ul>
    </li>
    <li><a href="#usage">Использование</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## О проекте

1. Создание пользователя
API принимает POST-запрос с именем пользователя и создает новую запись в базе данных с уникальным идентификатором и UUID токеном доступа. Данные сохраняются в базе данных и возвращаются в ответе на запрос.

2. Добавление аудиозаписи
API принимает POST-запрос с уникальным идентификатором пользователя, токеном доступа в заголовке запроса и аудиозаписью в формате wav. Аудиозапись преобразуется в формат mp3, генерируется уникальный UUID идентификатор и сохраняются в базе данных. Для скачивания записи генерируется URL который возвращается в ответе на запрос.

3. Доступ к аудиозаписи
API предоставляет GET-запрос для скачивания аудиозаписи по URL, сгенерированному в предыдущем шаге. При обращении к данному URL происходит загрузка аудиозаписи в формате mp3, которая может быть прослушана или сохранена на устройстве пользователя.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Технологии

Технологии которые использовались в этом проекте

* [![FastAPI][FastAPI]][FastAPI-url]
* [![SQLAlchemy][SQLAlchemy]][SQLAlchemy-url]
* [![Alembic][Alembic]][Alembic-url]
* [![Pydantic][Pydantic]][Pydantic-url]
* [![Pydub][Pydub]][Pydub-url]
* [![Aiofiles][Aiofiles]][Aiofiles-url]


* [![Docker][Docker]][Docker-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Подготовка и запуск

### Предварительные условия
У вас должны быть установленны следущие приложения

* docker
* docker-compose

### Как запустить

1. Скопируйте репозиторий
   ```sh
   git clone https://github.com/RezuanDzibov/bewise_test_2
   ```
2. Перейдите в директорию проекта

3. Переименуйте.env.template в .env следующей командой
<br>
    Windows 
    ```sh
     copy .env.template .env
    ```
   
    Linux/MacOS 
    ```sh
     cp .env.template .env
    ```

4. Запускаем
   ```sh
   docker-compose up --build
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Примеры запросов


Добавление пользователя

![add_user]

Использование токена, для доступа к инпуту справа сверху кнопка Authorize

![access_token_input]

Добавление аудиофайла 

![add_audiotrack]

Ендпоинт для скачивания файла

![audiotrack_file]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[add_audiotrack]: images/add_audiotrack.jpeg
[add_user]: images/add_user.jpeg
[access_token_input]: images/access_token_input.jpeg
[audiotrack_file]: images/get_audiotrack_file.jpeg
[FastAPI]: https://img.shields.io/badge/fastapi-05998b?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[SQLAlchemy]: https://img.shields.io/badge/sqlalchemy-778876?style=for-the-badge&logo=python&logoColor=black
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[Alembic]: https://img.shields.io/badge/alembic-6ba81d?style=for-the-badge&logo=python&logoColor=black
[Alembic-url]: https://alembic.sqlalchemy.org/en/latest/
[Pydantic]: https://img.shields.io/badge/Pydantic-e92064?style=for-the-badge&logo=python&logoColor=black
[Pydantic-url]: https://docs.pydantic.dev/latest/
[Pydub]: https://img.shields.io/badge/Pydub-ffffff?style=for-the-badge&logo=python&logoColor=black
[Pydub-url]: https://alembic.sqlalchemy.org/en/latest/
[Aiofiles]: https://img.shields.io/badge/Aiofiles-ffffff?style=for-the-badge&logo=python&logoColor=black
[Aiofiles-url]: https://github.com/Tinche/aiofiles
[Docker]: https://img.shields.io/badge/Docker-230db7?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-233161?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
