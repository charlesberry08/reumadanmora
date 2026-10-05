#!/usr/bin/env python3
"""Servidor estático de desarrollo sin caché (para la vista previa local)."""
import os, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class SinCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))

os.chdir(os.path.dirname(os.path.abspath(__file__)))
puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 4328
ThreadingHTTPServer(('127.0.0.1', puerto), SinCache).serve_forever()
