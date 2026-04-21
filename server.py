import socket
import hashlib

HOST, PORT, BUFSIZE = 'localhost', 5050, 4096
ADDRESS = (HOST, PORT)
USERS_FILE = "users.txt"
JOBS_FILE = "military_jobs.txt"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def correct_login(username, password):
    try:
        with open(USERS_FILE, "r") as file:
            users = dict(line.strip().split(",") for line in file)
            return users.get(username) == hash_password(password)
    except FileNotFoundError:
        pass

    with open(USERS_FILE, "a") as file:
        file.write(f"{username},{hash_password(password)}\n")
    return True


def load_jobs():
    jobs = {}
    try:
        with open(JOBS_FILE, "r") as file:
            for line in file:
                branch, job, desc = line.strip().split(",", 2)
                jobs.setdefault(branch, {})[job] = desc
    except FileNotFoundError:
        print("Jobs file not found.")
    return jobs


def handle_client(client_socket, military_positions):
    client_socket.send(b"Enter Username: ")
    username = client_socket.recv(BUFSIZE).decode().strip()
    client_socket.send(b"Enter Password: ")
    password = client_socket.recv(BUFSIZE).decode().strip()

    if not correct_login(username, password):
        client_socket.send(b"Login Failed...\n")
        client_socket.close()
        return

    while True:
        client_socket.send(b"Enter a branch (Army, Navy, Air Force, Marines) or press Enter to quit:\n")
        branch = client_socket.recv(BUFSIZE).decode().strip().title()

        if branch == '':
            break

        if branch in military_positions:
            jobs = "\n".join(f"- {job}: {desc}" for job, desc in military_positions[branch].items())
            client_socket.send(f"\n{branch} Jobs:\n{jobs}\n".encode())
        else:
            client_socket.send(b"Invalid branch selection.\n")

    client_socket.close()


military_positions = load_jobs()
server = socket.socket()
server.bind(ADDRESS)
server.listen()

print("Server is running...")

while True:
    client_socket, _ = server.accept()
    handle_client(client_socket, military_positions)
