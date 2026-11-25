#!/usr/bin/env python3
"""SDA Media Server - lance un serveur web local pour Media SDA Ambolokandrina.
Usage : double-clic sur sdaa.bat (qui appelle ce script).
Le serveur sert le dossier courant et ouvre http://localhost:8000/index.html
Cela permet au Mode Étendre (projection 2ème écran) de fonctionner sous Chrome.
"""
import http.server
import socketserver
import webbrowser
import os
import sys
import threading
import time

PORT = 8000
ROOT = os.path.dirname(os.path.abspath(sys.executable))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, format, *args):
        pass  # silence


def main():
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print(f"[SDA Media] Serveur demarre : {url}")
        # Ouvre le navigateur apres un court delai
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[SDA Media] Arret du serveur.")
            sys.exit(0)


if __name__ == "__main__":
    main()
