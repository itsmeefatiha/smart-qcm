import socket
# Force the system to prefer IPv4 over IPv6
orig_getaddrinfo = socket.getaddrinfo

def filtered_getaddrinfo(*args, **kwargs):
    res = orig_getaddrinfo(*args, **kwargs)
    return [r for r in res if r[0] == socket.AF_INET]

socket.getaddrinfo = filtered_getaddrinfo
import os

from src import create_app

app = create_app()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug)