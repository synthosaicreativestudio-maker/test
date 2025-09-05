# test
>>>>>>> 6eff3e320eb9a623ac3081f83ad6576dc10ef955
# Marketing Test Project

Проект для автоматизации маркетинга с интеграцией Telegram бота, Context7 MCP, Google Sheets и веб-интерфейсом.

## Функциональность

### Журналы проекта и утилита добавления записей

В репозитории добавлены журналы и скрипт для удобной работы с ними:

- `logs/rules_log.md` — журнал правил проекта
- `logs/project_log.md` — журнал проекта (changelog, milestones)
- `logs/bot_functions_log.md` — журнал основных функций бота
- `scripts/add_log.py` — утилита для добавления записей в любой из журналов
- `logs/general_log.md` — общий лог для оперативных заметок и решений

### Файлы окружения и секреты

Файл `env` используется для хранения указаний на логи и настроек проекта (включая URL репозитория). По умолчанию в `env` указана ссылка на репозиторий:

```
GITHUB_REPO=https://github.com/synthosaicreativestudio-maker/test
```

Файл `env` не должен коммититься в публичные репозитории. В репозитории также добавлен `env.example` — используйте его как шаблон и заполните реальные токены локально.

### Google Sheets и авторизация

Для автоматической записи статуса авторизации в Google Sheets требуется сервисный аккаунт с правами на редактирование таблицы. Поместите JSON учетных данных в файл и укажите путь в `env`:

```
GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
SHEET_ID=1_SB04LMuGB7ba3aog2xxN6N3g99ZfOboT-vdWXxrh_8
```

### Context7 MCP Integration

Проект использует Context7 как MCP-сервер для обогащения подсказок актуальной документацией.
Вместо установки Node.js-пакета, мы используем HTTP-интеграцию. Добавлен модуль `src/mcp/context7_client.py`.

Чтобы включить интеграцию:
1) Укажите URL вашего Context7 сервера в `env` переменной `CONTEXT7_URL`.
2) Установите зависимости: `pip install -r requirements.txt` (включён `httpx`).
3) Используйте в коде:

```python
from src.mcp.context7_client import Context7Client
client = Context7Client(CONTEXT7_URL)
res = await client.search('how to use aiogram')
```

### Local MCP

Если вы поместили реализацию MCP в проект (например `mcp_context_v7.py`), используйте обёртку `src/mcp/local_context.py` для взаимодействия:

```python
from src.mcp.local_context import create_thread_for_user, append_message, get_context_summary
tid = create_thread_for_user('telegram_123')
append_message(tid, 'user', 'Привет')
print(get_context_summary(tid))
```

### Web UI

Добавлена папка `web_ui` с готовыми стилями `styles.css` и примером страницы авторизации `auth.html`.
Это можно использовать как миниапп-страницу Telegram Web App или как отдельную страницу авторизации.

Чтобы запустить локально:

```bash
python3 scripts/serve_web.py --port 8000
# затем открыть http://localhost:8000/auth.html
```

## Примеры использования

```bash
python3 scripts/add_log.py --log logs/project_log.md --author "Иван" --type add --message "Добавил начальный план"
```

## Рекомендации

- Используйте читаемые и структурированные записи.
- Не храните секреты в журналах в репозитории.
- Версионируйте изменения через Git.
=======
# test
>>>>>>> 6eff3e320eb9a623ac3081f83ad6576dc10ef955
