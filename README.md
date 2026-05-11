# t-me

<div align="center">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="img/logo-dark.svg">
        <source media="(prefers-color-scheme: light)" srcset="img/logo-light.svg">
        <img alt="t-me logo" src="img/logo-light.svg" width="250" style="max-width: 100%;">
    </picture>
</div>

[![GitHub Release](https://img.shields.io/github/v/release/austnv/t-me?color=purple)](https://github.com/austnv/t-me/releases/latest)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

FastAPI сервис для конвертации Telegram ссылок `t.me` в диплинки `tg://`.

Открывайте любые Telegram-ссылки напрямую в приложении, минуя браузер и обходя блокировки — без VPN.

## Зачем это нужно

В России Telegram заблокирован, и ссылки `t.me` не открываются в браузере без VPN. Но само приложение работает у многих через прокси. Этот сервис превращает обычные ссылки в диплинки `tg://`, которые сразу открываются в приложении Telegram на любом устройстве.

## Как это работает

Вы заменяете домен в любой Telegram-ссылке:

| Обычная ссылка | Ваша ссылка |
|----------------|-------------|
| `t.me/durov` | `t.domain.me/durov` |
| `t.me/+79991234567` | `t.domain.me/+79991234567` |
| `t.me/addstickers/emoji` | `t.domain.me/addstickers/emoji` |
| `t.me/durov/123` | `t.domain.me/durov/123` |
| `t.me/boost/channel` | `t.domain.me/boost/channel` |

Сервис перенаправляет на соответствующий `tg://` диплинк, который открывается прямо в приложении.

## Поддерживаемые типы ссылок

Все типы ссылок реализованы в соответствии с [официальной документацией Telegram](https://core.telegram.org/api/links):

### Пользователи и чаты
- `/{username}` — публичные профили, каналы, группы
- `/+{phone}` — поиск по номеру телефона
- `/{username}?profile` — профиль пользователя
- `/{username}?direct` — монофорум (чат канала)

### Приглашения
- `/joinchat/{hash}` — пригласительные ссылки (старый формат)
- `/+{hash}` — пригласительные ссылки (новый формат)
- `/addlist/{slug}` — папки с чатами

### Сообщения и темы
- `/{username}/{message_id}` — ссылка на сообщение в публичном чате
- `/c/{channel_id}/{message_id}` — ссылка на сообщение в приватном чате
- `/{username}/{thread_id}/{message_id}` — сообщение в треде

### Боты и мини-приложения
- `/{bot}?start={param}` — запуск бота с параметром
- `/{bot}?startgroup` — добавление бота в группу
- `/{bot}/{app}` — прямые мини-приложения
- `/{bot}?startapp` — главное мини-приложение

### Медиа и контент
- `/{username}/s/{story_id}` — истории
- `/{username}/a/{album_id}` — альбомы историй
- `/addstickers/{slug}` — наборы стикеров
- `/addemoji/{slug}` — наборы эмодзи
- `/addtheme/{name}` — темы оформления

### Звонки и трансляции
- `/{username}?videochat` — видеозвонки
- `/{username}?livestream` — прямые трансляции
- `/call/{slug}` — конференц-звонки

### Прочее
- `/boost/{username}` — буст канала
- `/proxy` — MTProxy/Socks5 прокси
- `/login/{code}` — код входа
- `/invoice/{slug}` — счета на оплату
- `/setlanguage/{slug}` — языковые пакеты
- `/confirmphone` — подтверждение номера
- `/giftcode/{slug}` — подарочные коды Premium
- `/nft/{slug}` — коллекционные подарки
- `/m/{slug}` — бизнес-чаты
- `/bg/{params}` — обои (все типы)
- `/share` — поделиться сообщением

## Быстрый старт

### Docker

```bash
docker run -d -p 1234:1234 ghcr.io/austnv/t-me:latest
```

### Docker Compose

```bash
git clone https://github.com/austnv/t-me.git
cd t-me
docker compose up -d
```

### Ручной запуск

```bash
git clone https://github.com/austnv/t-me.git
cd t-me
uv sync
uv run fastapi run --port 1234
```

## Продакшен

Рекомендуется использовать за reverse-прокси (Caddy, Nginx) с HTTPS.

### Caddy

```caddy
t.domain.me {
    reverse_proxy localhost:1234
}
```

### Nginx

```nginx
server {
    listen 80;
    server_name t.domain.me;

    location / {
        proxy_pass http://localhost:1234;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## API

Сервис не имеет собственного API — он просто редиректит HTTP-запросы на соответствующие `tg://` URI.

### Коды ответов

| Код | Описание |
|-----|----------|
| `307` | Успешный редирект на `tg://` диплинк |
| `404` | Ссылка не распознана |

## Разработка

```bash
git clone https://github.com/austnv/t-me.git
cd t-me
uv sync
uv run fastapi dev
```

Сервер разработки с hot-reload будет доступен на `http://localhost:8000`.

## Технологии

- [FastAPI](https://fastapi.tiangolo.com/) — веб-фреймворк
- [uv](https://docs.astral.sh/uv/) — пакетный менеджер
- [Docker](https://www.docker.com/) — контейнеризация
- [Python 3.14](https://www.python.org/) — язык программирования

## Вклад в проект

Pull request'ы приветствуются. Для значительных изменений создавайте issue для обсуждения.

## Лицензия

MIT

## Ссылки

- [Официальная документация Telegram по диплинкам](https://core.telegram.org/api/links)
- [Образ на GitHub Container Registry](https://github.com/austnv/t-me/pkgs/container/t-me)