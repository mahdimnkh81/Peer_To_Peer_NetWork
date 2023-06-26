import http.client
import json
import socket
import datetime
import threading
import time

import redis

id = str(datetime.datetime.now())
# id = "qq"
PORT = 9191
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(hostname)
print(ip_address)

redis_host = 'localhost'
redis_port = 6379
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


def post_information():
    con = http.client.HTTPConnection(host='127.0.0.1', port=8031)
    id = input("ENTER YOUR NAME!!")
    ids = r.lrange('ids', 0, -1)
    flage = True
    while (flage):
        if id in ids:
            print("This name has already been chosen")
            print("Choose another name")
            id = input("ENTER YOUR NAME!!")
        else:
            flage = False
    body = {id: ip_address, "port": PORT, "hostname": hostname}
    json_body = json.dumps(body)
    headers = {'Content-type': f'{len(json_body)}'}
    con.request("Post", "http://localhost:8031/info", body=json_body, headers=headers)
    con.close()


def get_listOfClients():
    conn = http.client.HTTPConnection(host='127.0.0.1', port=8031)

    while 1:
        conn.request("GET", "http://localhost:8031/listOfclients")
        rsp = conn.getresponse()
        list_ids = list(rsp.headers.values())[2]
        x = str(list_ids)
        y = ""
        for i in x:
            if i != '[' and i != ']' and i != ',' and i != '"':
                y += i
        show_list_ids = y.split(" ")
        print(rsp.reason)
        for i in range(0, len(show_list_ids)):
            print(str(i) + "__>" + show_list_ids[i])
        name_of_client = input()
        post_chose_client(name_of_client)
        conn.close()
        break


def post_chose_client(id):
    conn = http.client.HTTPConnection(host='127.0.0.1', port=8031)
    body = {"name": id}
    json_body = json.dumps(body)
    headers = {'Content-type': f'{len(json_body)}'}
    conn.request("Post", "http://localhost:8031/choseClient", body=json_body, headers=headers)
    rsp = conn.getresponse()
    info = list(rsp.headers.values())[2]
    x = str(info)
    y = ""
    for i in x:
        if i != '[' and i != ']' and i != ',' and i != '"':
            y += i
    show_list_info = y.split(" ")
    print(rsp.reason)
    print("ipAddress" + "__>" + show_list_info[0])
    print("port" + "__>" + show_list_info[1])
    print("hostname" + "__>" + show_list_info[2])
    conn.close()
    connect_to_client(show_list_info[2], show_list_info[1], show_list_info[0])


def get_info_client():
    conn = http.client.HTTPConnection(host='127.0.0.1', port=8031)

    while 1:
        conn.request("GET", "http://localhost:8031/listOfclients")
        rsp = conn.getresponse()
        list_ids = list(rsp.headers.values())[2]
        x = str(list_ids)
        y = ""
        for i in x:
            if i != '[' and i != ']' and i != ',' and i != '"':
                y += i
        show_list_ids = y.split(" ")
        print(rsp.reason)
        for i in range(0, len(show_list_ids)):
            print(str(i) + "__>" + show_list_ids[i])
        name_of_client = input()
        post_chose_client(name_of_client)
        conn.close()
        break


def connect_to_client(hostname, port, ipaddress):
    client_socket = socket.socket()  # instantiate
    client_socket.connect((hostname, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    def handle_client(client_socket):

        with client_socket as sock:
            time.sleep(10)
            request = sock.recv(1024)
            # print(f'[*] Received: {request.decode("utf-8")}')
            sock.send(b'ACK')
            sock.close()


    host = socket.gethostname()
    port = 5000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)
    print(f'[*] Listening on {host}:{port}')

    while True:
        client, address = server.accept()

        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

    # host = socket.gethostname()
    # port = 5000  # initiate port no above 1024
    #
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind((host, port))
    #
    # server_socket.listen(5)
    # conn, address = server_socket.accept()  # accept new connection
    # print("Connection from: " + str(address))
    # while True:
    #     # receive data stream. it won't accept data packet greater than 1024 bytes
    #     data = conn.recv(1024).decode()
    #     if not data:
    #         # if data is not received break
    #         break
    #     print("from connected user: " + str(data))
    #     data = input(' -> ')
    #     conn.send(data.encode())  # send data to the client
    #
    # conn.close()  # close the connection
    # # post_information()
    # # get_listOfClients()

while 1:
    cmd = input('input command (ex. GET index.html): ')
    cmd = cmd.split()

    if cmd[0] == 'exit':  # tipe exit to end it
        break
