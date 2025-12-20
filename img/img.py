from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
from requests import get, put
import urllib.parse
import json

OAUTH_TOKEN = ""

def run(handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


class HttpGetHandler(BaseHTTPRequestHandler):

    def get_uploaded_files(self):
        """Получает список файлов, уже загруженных на Яндекс.Диск"""
        uploaded_files = []
        offset = 0
        limit = 100

        try:
            while True:
                # Запрашиваем метаинформацию о папке Backup с пагинацией
                resp = get(
                    "https://cloud-api.yandex.net/v1/disk/resources",
                    params={
                        "path": "Backup",
                        "fields": "_embedded.items.name",
                        "limit": limit,
                        "offset": offset
                    },
                    headers={"Authorization": "OAuth " + OAUTH_TOKEN}
                )

                if resp.status_code == 200:
                    data = json.loads(resp.text)

                    if "_embedded" in data and "items" in data["_embedded"]:
                        for item in data["_embedded"]["items"]:
                            uploaded_files.append(item["name"])

                    # Проверяем, есть ли еще файлы для загрузки
                    if len(data.get("_embedded", {}).get("items", [])) < limit:
                        break

                    offset += limit
                else:
                    print(f"Ошибка при запросе списка файлов: {resp.status_code}")
                    print(resp.text)
                    break

        except Exception as e:
            print(f"Исключение при получении списка файлов: {e}")

        return uploaded_files

    def do_GET(self):
        local_files = os.listdir("pdfs")

        uploaded_files = self.get_uploaded_files()

        def fname2html(fname):
            # Определяем стиль фона в зависимости от статуса загрузки
            if fname in uploaded_files:
                bg_style = "style='background-color: rgba(0, 200, 0, 0.25);'"
            else:
                bg_style = ""

            return f"""
                <li {bg_style} onclick="fetch('/upload', {{'method': 'POST', 'body': '{fname}'}}).then(() => location.reload())">
                    {fname}
                </li>
            """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html_content = """
            <html>
                <head>
                </head>
                <body>
                    <ul>
                      {files}
                    </ul>
                </body>
            </html>
        """.format(files="\n".join(map(fname2html, local_files)))

        self.wfile.write(html_content.encode())

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        fname = self.rfile.read(content_len).decode("utf-8")
        local_path = f"pdfs/{fname}"
        ya_path = f"Backup/{urllib.parse.quote(fname)}"

        # Получаем URL для загрузки
        resp = get(
            f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={ya_path}",
            headers={"Authorization": "OAuth " + OAUTH_TOKEN}
        )

        if resp.status_code == 200:
            upload_url = json.loads(resp.text)["href"]

            # Загружаем файл
            with open(local_path, 'rb') as f:
                resp = put(upload_url, files={'file': (fname, f)})

            print(f"Статус загрузки файла {fname}: {resp.status_code}")
        else:
            print(f"Ошибка получения URL для загрузки: {resp.status_code}")
            print(resp.text)

        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    oauth_token_input = input("Введите OAuth токен Яндекс.Диска: ").strip()
    OAUTH_TOKEN = oauth_token_input
    print(f"Токен сохранен")
    run(handler_class=HttpGetHandler)
