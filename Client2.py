import http.client
import json
import socket
import datetime
import threading
import time
import numpy as np
from PIL import Image
from numpy import array
import redis
import select

id = str(datetime.datetime.now())
PORT = 4521
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

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
    connect_to_client(show_list_info[2], show_list_info[1], show_list_info[0])
    conn.close()


# def get_info_client():
#     conn = http.client.HTTPConnection(host='127.0.0.1', port=8031)
#
#     while 1:
#         conn.request("GET", "http://localhost:8031/listOfclients")
#         rsp = conn.getresponse()
#         list_ids = list(rsp.headers.values())[2]
#         x = str(list_ids)
#         y = ""
#         for i in x:
#             if i != '[' and i != ']' and i != ',' and i != '"':
#                 y += i
#         show_list_ids = y.split(" ")
#         print(rsp.reason)
#         for i in range(0, len(show_list_ids)):
#             print(str(i) + "__>" + show_list_ids[i])
#         name_of_client = input()
#         conn.close()
#         post_chose_client(name_of_client)
#         break


def connect_to_client(hostname, port, ipaddress):
    question = input("Do you want to give or receive services?")
    if question == "receive":
        p = input("Do you want receive text or image?")
        if p == "text":
            server_TCP_text()
        else:
            server_UDP_image()
    else:
        result = input("Do you want send text or image?")
        if result == 'text':
          client_TCP_text(hostname, port, ipaddress)
        else:
          client_UDP_image(hostname, port, ipaddress)


def server_TCP_text():
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


def server_UDP_image():
    while True:
        localIP = "127.0.0.1"
        bufferSize = 16
        msgFromServer = "ACK"
        bytesToSend = str.encode(msgFromServer)
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((localIP, PORT))
        print("UDP server up and listening")
        recv = bytearray()
        x = []
        bytesAddressPair = UDPServerSocket.recvfrom(1024)
        address = bytesAddressPair[1]
        while recv != b'finish':
            recv = UDPServerSocket.recv(1024)
            array_recv = list(map(int, recv))
            x.append(array_recv)
            UDPServerSocket.sendto(bytesToSend, address)

        two_dim = []
        three_dim = []
        z = []
        c = 0
        for i in x:
            for j in i:
                if j != 0:
                    z.append(j)
            # print(z)
            two_dim.append(z)
            z = []
            c += 1
            if c == bufferSize:
                three_dim.append(two_dim)
                two_dim = []
                c = 0
        # print(three_dim)
        produce_image = np.array(three_dim, dtype=np.uint8)
        # print(type(final))
        pilImage = Image.fromarray(produce_image)
        pilImage.show()
        UDPServerSocket.close()


def client_TCP_text(hostname, port, ipaddress):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, int(port)))
    text = input("Enter your text")
    print("send...")
    s.send(text.encode("utf-8"))
    flag = ''
    while flag != "ACK":
        ready = select.select([s], [], [], 2)
        if ready[0]:
            response = s.recv(4096)
            flag = response.decode('utf-8')
            print(flag)
        else:
            print("timeout")
            print("send again...")
            s.send(text.encode("utf-8"))

    s.close()


def client_UDP_image(hostname, port, ipaddress):
    msgFromClient = input("Enter image")
    bytesToSend = str.encode(msgFromClient)
    serverAddressPort = ("127.0.0.1", int(port))
    bufferSize = 1024
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    s.sendto(bytesToSend, serverAddressPort)
    image = Image.open(r"C:\Users\Asus\Desktop\Screenshot 2023-06-26 165215.jpg")
    array_image = array(image)
    for i in array_image:
        k = 0
        for j in i:
            bytes_of_image = bytes(j) + bytes(k)
            k += 1
            s.sendto(bytes_of_image, serverAddressPort)
            msgFromServer = s.recvfrom(bufferSize)
            print(msgFromServer[0])
    s.sendto(bytes("finish".encode("utf-8")), serverAddressPort)


if __name__ == '__main__':
    # client_UDP_image()
    post_information()
    get_listOfClients()

while 1:
    cmd = input('input command (ex. exit): ')
    if cmd == 'exit':
        exit(0)
