"""ローカルホストで Pages のパスと 404 を模擬する。"""

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--base", default="/japan-infection-watch/")
    args = parser.parse_args()
    active = args.workspace / "active"

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *request):
            super().__init__(*request, directory=str(active))

        def translate_path(self, path):
            if args.base == "/":
                return super().translate_path(path)
            return super().translate_path(path[len(args.base) - 1:])

        def send_head(self):
            path = urlsplit(self.path).path
            if path == args.base.rstrip("/") and args.base != "/":
                self.send_response(301)
                self.send_header("Location", args.base)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            if not path.startswith(args.base):
                self.send_error(404, "Not Found")
                return None
            return super().send_head()

        def send_error(self, code, message=None, explain=None):
            custom = active / "404.html"
            if code == 404 and custom.is_file():
                data = custom.read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(data)
                return
            super().send_error(code, message, explain)

        def log_message(self, *_):
            pass

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        print(f"http://127.0.0.1:{server.server_port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
