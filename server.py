#!/usr/bin/env python3
"""HTTP server for LogisticForce Data 360 Workshop. Works locally and on Heroku."""
import http.server, socketserver, os, functools

PORT = int(os.environ.get("PORT", 5050))
ROOT = os.path.dirname(os.path.abspath(__file__))

Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)

print(f"📂  Sirviendo: {ROOT}")
print(f"🚀  Workshop en  http://0.0.0.0:{PORT}")
print(f"    Ctrl+C para detener\n")

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹  Servidor detenido.")
