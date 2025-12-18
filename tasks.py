from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os

TASKS = []
NEXT_TASK_ID = 1
FILE_NAME = 'tasks.txt'


class TaskServer(BaseHTTPRequestHandler):

    def _read_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length) if length > 0 else b""
        if not raw:
            return None
        try:
            return json.loads(raw)
        except:
            return None

    def _send_json(self, data, status=200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/tasks":
            self._send_json(TASKS)
        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        parts = parsed.path.split("/")

        if parsed.path == "/tasks":
            self._create_task()
        elif len(parts) == 4 and parts[1] == "tasks" and parts[3] == "complete":
            try:
                task_id = int(parts[2])
                self._complete_task(task_id)
            except:
                self._send_json({"error": "Не верный ID"}, 400)
        else:
            self._send_json({"error": "Not found"}, 404)

    def _create_task(self):
        global TASKS, NEXT_TASK_ID

        data = self._read_json_body()

        if not data or "title" not in data or "priority" not in data:
            self._send_json({"error": "Поле 'title' или 'priority' не заполнено"}, 400)
            return

        if data["priority"] not in ["low", "normal", "high"]:
            self._send_json({"error": "Поле 'priority' должно быть low, normal или high"}, 400)
            return

        task = {
            "id": NEXT_TASK_ID,
            "title": data["title"],
            "priority": data["priority"],
            "isDone": False
        }

        TASKS.append(task)
        NEXT_TASK_ID += 1

        try:
            with open(FILE_NAME, 'w', encoding='utf-8') as f:
                json.dump(TASKS, f, ensure_ascii=False)
        except:
            pass

        self._send_json(task, 201)

    def _complete_task(self, task_id):
        global TASKS

        for task in TASKS:
            if task["id"] == task_id:
                task["isDone"] = True

                try:
                    with open(FILE_NAME, 'w', encoding='utf-8') as f:
                        json.dump(TASKS, f, ensure_ascii=False)
                except:
                    pass

                self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return

        self._send_json({"error": "Not found"}, 404)


def load_tasks():
    global TASKS, NEXT_TASK_ID

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                data = f.read()
                if data:
                    TASKS = json.loads(data)
                    if TASKS:
                        NEXT_TASK_ID = max(task['id'] for task in TASKS) + 1
        except:
            TASKS = []


def run(host="", port=8080):
    load_tasks()

    server = HTTPServer((host, port), TaskServer)
    server.serve_forever()


if __name__ == "__main__":
    run()