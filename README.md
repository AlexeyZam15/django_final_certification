# 🍳 Сайт рецептов (recipessite)

Итоговая аттестационная работа по программе **«Веб-разработка на Python»**.

Проект представляет собой веб-приложение для публикации и просмотра кулинарных рецептов: пользователи могут регистрироваться, добавлять собственные рецепты с форматированным описанием и изображениями, объединять рецепты по категориям, а администратор — управлять контентом через встроенную админ-панель Django.

📥 **Готовая сборка (`.rar` с папкой `dist`):** [скачать](https://github.com/AlexeyZam15/django_final_certification/releases/download/latest/recipessite.rar)

> **Важно про хостинг:** публичного хостинга у проекта сейчас **нет** (ранее размещённая версия на PythonAnywhere недоступна). Проект полностью работоспособен **локально** и в виде **desktop-сборки** (`.exe`). Инструкции по запуску — ниже.

---

## 🛠 Использованные технологии

### Backend
- **Python 3.14** — язык разработки.
- **Django 5.0.3** — веб-фреймворк (ORM, маршрутизация, шаблоны, админ-панель, аутентификация).
- **SQLite** (`db.sqlite3`) — реляционная база данных (в проекте используется по умолчанию).
- **python-dotenv** — загрузка переменных окружения из `.env`.
- **Django ORM** — работа с моделями `Recipe`, `Category`, `RecipeCategory`.

### Frontend
- **HTML5**, **CSS3**.
- **Bootstrap 5.0.2** (CDN) — адаптивная вёрстка, карточки, навигация, пагинация.
- **Django Templates** — серверный рендеринг страниц.
- **JavaScript** (минимально) — интерактивные элементы интерфейса (подтверждения удаления, навигация).
- **Django CKEditor** (`django-ckeditor 6.7.1`) — WYSIWYG-редактор для полей «Описание» и «Шаги приготовления».

### Инструменты разработки
- **django-debug-toolbar 4.3.0** — профилирование запросов (включается только в `DEBUG` и вне desktop-режима).
- **Pillow** — обработка изображений (`ImageField`).
- **Git** — контроль версий.

### Desktop-сборка
- **PyInstaller 6.x** — упаковка загрузчика в `.exe`.
- **tkinter** — GUI-окно лаунчера (статус, кнопка Stop, терминал с логом).
- **Собственный `build_exe.py`** — сборка `recipessite.exe` (loader + `.venv` + файлы проекта) и `run.py` — запуск Django в desktop-режиме.

---

## ✨ Функционал

### Для пользователя
- **Регистрация, вход и выход** (Django auth).
- **Просмотр списка рецептов** с пагинацией.
- **Просмотр страницы рецепта**: название, изображение, описание (CKEditor), шаги приготовления, время, автор, даты создания/изменения, категории.
- **Категории**: список категорий и рецепты внутри выбранной категории.
- **Добавление рецепта** авторизованным пользователем: название, описание, шаги, время, изображение, категории.
- **Редактирование и удаление** рецепта — доступно **автору** или **суперпользователю**.
- **Адаптивный интерфейс** (Bootstrap): карточки рецептов, меню, пагинация.

### Для администратора
- **Django Admin**: управление рецептами, категориями, связями, пользователями.
- **Модерация контента**: редактирование/удаление любых рецептов.
- **Debug Toolbar** (только dev): SQL-запросы, шаблоны, кэш, сигналы.

---

## 📸 Скриншоты

<table>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/AlexeyZam15/django_final_certification/refs/heads/main/screenshots/2026-10-28_16-43-36.png" width="400" alt="Скриншот 1"><br>Скриншот 1</td>
    <td align="center"><img src="https://raw.githubusercontent.com/AlexeyZam15/django_final_certification/refs/heads/main/screenshots/2026-10-28_16-43-47.png" width="400" alt="Скриншот 2"><br>Скриншот 2</td>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/AlexeyZam15/django_final_certification/refs/heads/main/screenshots/2026-10-28_16-44-03.png" width="400" alt="Скриншот 3"><br>Скриншот 3</td>
    <td align="center"><img src="https://raw.githubusercontent.com/AlexeyZam15/django_final_certification/refs/heads/main/screenshots/2026-10-28_16-44-18.png" width="400" alt="Скриншот 4"><br>Скриншот 4</td>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/AlexeyZam15/django_final_certification/refs/heads/main/screenshots/2026-10-28_16-44-26.png" width="400" alt="Скриншот 5"><br>Скриншот 5</td>
    <td align="center"><img src="https://raw.githubusercontent.com/AlexeyZam15/django_final_certification/refs/heads/main/screenshots/2026-10-28_16-44-42.png" width="400" alt="Скриншот 6"><br>Скриншот 6</td>
  </tr>
  <tr>
    <td align="center" colspan="2"><img src="https://raw.githubusercontent.com/AlexeyZam15/django_final_certification/refs/heads/main/screenshots/2026-10-28_16-44-50.png" width="400" alt="Скриншот 7"><br>Скриншот 7</td>
  </tr>
</table>

---

## 🧩 Что было сделано в рамках аттестационной работы

1. **Спроектирована структура проекта**: Django-проект `recipessite` с приложениями `recipes` (рецепты, категории) и `users` (пользователи).
2. **Реализованы модели**:
   - `Recipe` — рецепт (название, описание, шаги, время, изображение, автор, даты, категории).
   - `Category` — категория рецептов.
   - `RecipeCategory` — связующая таблица «многие ко многим» между рецептами и категориями.
3. **Реализованы представления и маршруты**: список рецептов, страница рецепта, CRUD рецептов, категории, аутентификация.
4. **Свёрстаны шаблоны** на Bootstrap 5: базовый шаблон, список рецептов, страница рецепта, форма рецепта, категории, пагинация, меню.
5. **Интегрирован CKEditor** для форматированного ввода описания и шагов приготовления.
6. **Настроена загрузка изображений** (`MEDIA_ROOT`, `MEDIA_URL`).
7. **Ограничены права**: редактирование/удаление рецепта — только автор или суперпользователь.
8. **Настроена админ-панель Django** для управления контентом.
9. **Подготовлена desktop-версия**: `run.py` (GUI-лаунчер с кнопкой Stop и терминалом) и `build_exe.py` (сборка `recipessite.exe` через PyInstaller с bundled `.venv`).
10. **Оформлена документация** (этот `README.md`) и подготовлен проект к сдаче.

---

## 📁 Структура проекта

```

recipessite/
├── manage.py
├── run.py # GUI-лаунчер для desktop-режима
├── build_exe.py # Сборка recipessite.exe
├── requirements.txt
├── db.sqlite3 # SQLite-БД
├── .env # Переменные окружения (в сборку не копируется)
├── recipessite/ # Настройки проекта
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── recipes/ # Приложение «Рецепты»
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── templates/recipes/
├── users/ # Приложение «Пользователи»
├── templates/ # Общие шаблоны (base.html, includes/)
├── static/ # CSS, JS, изображения
└── media/ # Загруженные изображения рецептов

```

---

## 🚀 Запуск локально (рекомендуется)

### 1. Клонировать репозиторий и перейти в папку проекта
```bash
cd recipessite
```

### 2. Создать и активировать виртуальное окружение

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать `.env` в корне проекта

```env
SECRET_KEY=your-secret-key-here
```

> `SECRET_KEY` можно сгенерировать командой:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Применить миграции

```bash
python manage.py migrate
```

### 6. (Опционально) Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запустить сервер

```bash
python manage.py runserver
```

Откройте в браузере: **http://127.0.0.1:8000/**

---

## 🖥 Desktop-сборка (`.exe`)

Проект можно собрать в автономный `.exe` (Windows), который запускает Django локально с GUI-окном.

### 📥 Готовая сборка (скачать)

Не хотите собирать вручную — скачайте готовый архив с папкой `dist`:

🔗 **Скачать `recipessite.rar`:
** [https://github.com/AlexeyZam15/django_final_certification/releases/download/latest/recipessite.rar](https://github.com/AlexeyZam15/django_final_certification/releases/download/latest/recipessite.rar)

**Инструкция:**

1. Скачайте `recipessite.rar`.
2. Распакуйте архив в любую папку (например, `C:\recipessite\`).
3. Запустите `recipessite.exe` из распакованной папки — откроется окно лаунчера, приложение будет доступно по адресу *
   *http://127.0.0.1:8000/**.
4. Для остановки — кнопка **Stop** в окне лаунчера или закрытие окна.

> ⚠️ Примечание: `.exe` собран через PyInstaller, некоторые антивирусы (например, 360 Total Security) могут выдавать *
*ложное срабатывание**. При необходимости добавьте папку с распакованным архивом в исключения антивируса.

### 🔧 Собрать самостоятельно

```bash
python build_exe.py
```

Результат: `dist/recipessite/recipessite.exe` (loader) + `.venv/` + файлы проекта.

### Запуск

Дважды кликнуть `dist/recipessite/recipessite.exe` — откроется окно лаунчера с кнопкой **Stop** и терминалом; приложение
будет доступно по адресу **http://127.0.0.1:8000/**.

---

## 🌐 Статус хостинга

- **Публичный хостинг:** на данный момент **отсутствует** (ранее размещённая версия на PythonAnywhere недоступна).
- **Локальная версия:** полностью работоспособна, запускается по инструкции выше.
- **Desktop-версия:** собирается в `.exe` и работает автономно на Windows. Готовый архив — в
  разделе [«Готовая сборка (скачать)»](#-desktop-сборка-exe).

---

## 📌 Ограничения и планы развития

- Сейчас используется **SQLite**; в перспективе — переход на **PostgreSQL** (код частично подготовлен).
- Планируется добавить **поиск** по рецептам и **фильтры** по категориям/времени приготовления.
- Планируется **деплой** на публичный хостинг (PythonAnywhere / Railway / VPS).
- Планируется добавление **API** (Django REST Framework) для мобильного клиента.

---

## 👤 Автор

**Алексей Замараев**  
Итоговая аттестационная работа по программе «Веб-разработка на Python».

> Проект создан в учебных целях и демонстрирует навыки разработки full-stack веб-приложений на Django: проектирование
моделей и БД, представления и маршрутизация, шаблоны и вёрстка, аутентификация и права доступа, интеграция сторонних
библиотек (CKEditor, Debug Toolbar), а также подготовка desktop-сборки.
