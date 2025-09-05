# Журналы проекта и утилита добавления записей

В репозитории добавлены журналы и скрипт для удобной работы с ними:

- `logs/rules_log.md` — журнал правил проекта
- `logs/project_log.md` — журнал проекта (changelog, milestones)
- `logs/bot_functions_log.md` — журнал основных функций бота
- `scripts/add_log.py` — утилита для добавления записей в любой из журналов
 - `logs/general_log.md` — общий лог для оперативных заметок и решений

Файлы окружения и секреты
-------------------------
Файл `env` используется для хранения указаний на логи и настроек проекта (включая URL репозитория). По умолчанию в `env` указана ссылка на репозиторий, который вы попросили установить:

GITHUB_REPO=https://github.com/synthosaicreativestudio-maker/test

Файл `env` не должен коммититься в публичные репозитории. В репозитории также добавлен `env.example` — используйте его как шаблон и заполните реальные токены локально.

Файл `.gitignore` настроен так, чтобы исключать `env` и похожие файлы из коммитов.

Google Sheets и авторизация
---------------------------
Для автоматической записи статуса авторизации в Google Sheets требуется сервисный аккаунт с правами на редактирование таблицы. Поместите JSON учетных данных в файл и укажите путь в `env`:

GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
SHEET_ID=1_SB04LMuGB7ba3aog2xxN6N3g99ZfOboT-vdWXxrh_8

Если сервисный аккаунт не настроен, бот попытается выполнить поиск, но не сможет обновить таблицу; в этом случае он уведомит администратора / запишет событие в `logs/general_log.md`.

Context7 MCP (Context7)
-----------------------
Проект использует Context7 как MCP-сервер для обогащения подсказок актуальной документацией.
Вместо установки Node.js-пакета, мы используем HTTP-интеграцию. Добавлен модуль `src/mcp/context7_client.py`.

Чтобы включить интеграцию:
1) Укажите URL вашего Context7 сервера в `env` переменной `CONTEXT7_URL`.
2) Установите зависимости: `pip install -r requirements.txt` (включён `httpx`).
3) Используйте в коде:

```py
from src.mcp.context7_client import Context7Client
client = Context7Client(CONTEXT7_URL)
res = await client.search('how to use aiogram')
```

Если вы используете публичный Context7 сервис, убедитесь, что он доступен и открыт для запросов с вашего хоста.

Local MCP
---------
Если вы поместили реализацию MCP в проект (например `mcp_context_v7.py`), используйте обёртку `src/mcp/local_context.py` для взаимодействия:

```py
from src.mcp.local_context import create_thread_for_user, append_message, get_context_summary
tid = create_thread_for_user('telegram_123')
append_message(tid, 'user', 'Привет')
print(get_context_summary(tid))
```

Файл `mcp_context_v7.py` уже присутствует в проекте и предоставляет хранение контекста и persistence.

Web UI / CSS module
--------------------
Добавлена папка `web_ui` с готовыми стилями `styles.css` и примером страницы авторизации `auth.html`.
Это можно использовать как миниапп-страницу Telegram Web App или как отдельную страницу авторизации.

Чтобы запустить локально:

```bash
python3 scripts/serve_web.py --port 8000
# затем открыть http://localhost:8000/auth.html
```

Страница имеет простую клиентскую валидацию и демонстрационный POST на `/authorize`.

Примеры использования утилиты:

```bash
python3 scripts/add_log.py --log logs/project_log.md --author "Иван" --type add --message "Добавил начальный план"
```

Рекомендации:
- Используйте читаемые и структурированные записи.
- Не храните секреты в журналах в репозитории.
- Версионируйте изменения через Git.
