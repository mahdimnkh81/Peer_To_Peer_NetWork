import json
from http.server import HTTPServer, BaseHTTPRequestHandler

import redis

redis_host = 'localhost'
redis_port = 6379

redis_query = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


class EchoHandeler(BaseHTTPRequestHandler):
    def do_Post(self):
        print("Post")
        if self.path.endswith("/info"):
            content_length = int(self.headers['Content-type'])
            post_data = self.rfile.read(content_length)
            x = json.loads(post_data.decode())
            id = list(x.keys())[0]
            port = list(x.keys())[1]
            hostname = list(x.keys())[2]
            ip_client = x[id]
            port_client = x[port]
            hostname_client = x[hostname]
            redis_query.rpush(id, ip_client, port_client, hostname_client)
            redis_query.rpush('ids', id)

        if self.path.endswith("/choseClient"):
            print("/choseClient")
            content_length = int(self.headers['Content-type'])
            post_data = self.rfile.read(content_length)
            x = json.loads(post_data.decode())
            id = list(x.keys())[0]
            id_client = x[id]
            info_client = redis_query.lrange(id_client, 0, -1)
            print(info_client)
            try:
                # send code 200 response
                self.send_response(200, message="The information required to connect to the system")

                # send header first
                # self.send_header(ids, 'text-html')
                # self.send_response(ids)
                json_info_client = json.dumps(info_client)
                self.send_header('infoClient', json_info_client)
                self.end_headers()

            except IOError:
                self.send_error(404, 'file not found')


    def do_GET(self):
        if self.path.endswith("/listOfclients"):
            print("GET")
            ids = redis_query.lrange('ids', 0, -1)
            print(ids)
            print(ids[2])

            # self.send_response(code=200,  message="ssss")
            # self.request()
            try:
                # send code 200 response
                self.send_response(200, message="Which system do you want to connect to?")

                # send header first
                # self.send_header(ids, 'text-html')
                # self.send_response(ids)
                json_ids = json.dumps(ids)
                self.send_header('ids', json_ids)
                self.end_headers()

            except IOError:
                self.send_error(404, 'file not found')




def main():
    PORT = 8031
    server_address = ('127.0.0.1', PORT)
    server = HTTPServer(server_address, EchoHandeler)
    print('Server running on port %s' % PORT)
    server.serve_forever()


if __name__ == '__main__':
    main()
