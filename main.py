import socket


def emit_message(request_data, type="CONNECTION"):

    if type == "CONNECTION":
        print()
        print()
        print("NEW CONNECTION MADE".center(20, "#"))
        print()

        print()
        print(request_data)
        print()


def server():

    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print(f"SERVER IS LISTENING ON {SERVER_PORT}...\n\n")

    try:
        while True:
            # This is a blocking task that waits for connections.
            client_connection, _ = server_socket.accept()

            request = client_connection.recv(1024).decode()
            emit_message(request, "CONNECTION")

            headers = request.split("\n")
            fileName = headers[0].split()[1]

            if fileName == "/":
                fileName = "index.html"
            elif fileName[0] == "/":
                fileName = fileName[1:]

            try:
                print(f"FILENAME IS: {fileName}")
                cin = open(file=fileName)
                content = cin.read()
                cin.close()

                response = f"HTTP/1.0 200 OK\n\n{content}"
            except Exception as e:
                print(e)
                response = f"HTTP/1.0 404 NOT FOUND\n\nFILE NOT FOUND"
            finally:
                client_connection.sendall(response.encode())

            client_connection.close()

    finally:
        server_socket.close()


server()
