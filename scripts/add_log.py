#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой скрипт для добавления записей в журналы проекта.
Пример использования:
python3 scripts/add_log.py --log logs/project_log.md --author "Иван" --type update --message "Добавил план релиза"
"""
import argparse
import datetime
import os
import sys


def iso_now():
    return datetime.datetime.now().astimezone().isoformat()


def append_entry(path, author, typ, message):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    ts = iso_now()
    entry = f"\n---\nДата: {ts}\nАвтор: {author}\nДействие: {typ}\n\n{message}\n---\n"
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(entry)
    except Exception as e:
        print(f"Ошибка при записи в {path}: {e}")
        sys.exit(2)
    print(f"Запись добавлена в {path}")


def main():
    parser = argparse.ArgumentParser(description='Добавить запись в журнал проекта')
    parser.add_argument('--log', required=True, help='Путь к файлу журнала (например logs/project_log.md)')
    parser.add_argument('--author', default='unknown', help='Имя автора')
    parser.add_argument('--type', default='update', help='Тип действия: add|update|fix|note')
    parser.add_argument('--message', required=True, help='Текст записи')
    args = parser.parse_args()
    append_entry(args.log, args.author, args.type, args.message)


if __name__ == '__main__':
    main()
