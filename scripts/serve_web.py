#!/usr/bin/env python3
"""Простой статический HTTP-сервер для локальной проверки `web_ui`.

Запуск:
  python3 scripts/serve_web.py --port 8000

Сервер будет обслуживать каталог `web_ui` на корневом пути. Это удобно для тестирования миниаппов и страницы авторизации.
"""
import argparse
import http.server
import socketserver
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()

    webdir = os.path.join(os.getcwd(), 'web_ui')
    if not os.path.isdir(webdir):
        print('Каталог web_ui не найден')
        return

    os.chdir(webdir)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(('', args.port), handler) as httpd:
        print(f'Сервер запущен: http://localhost:{args.port}/auth.html')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Остановлен')


if __name__ == '__main__':
    main()
