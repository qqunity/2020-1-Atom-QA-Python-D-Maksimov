import socket
import json


def response_parser(data):
    data = ''.join(data)
    body = data.split('\r\n\r\n')[1]
    data = data.split('\r\n\r\n')[0]
    data = data.split('\r\n')
    response_code = int(data[0].split()[1])
    headers = dict()
    for line in data:
        if ':' in line:
            line = line.split(':')
            sub_line = line[1:]
            sub_line = ''.join(sub_line)
            if not ('{' in line[0] or '}' in line[0]):
                headers[line[0]] = sub_line[1:]
    if headers['Content-Type'] == 'application/json':
        body = json.loads(body)
    response = {'response_code': response_code, 'headers': headers, 'body': body}
    return response


class HttpClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def open_connection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(0.1)
        self.client.connect((self.host, self.port))

    def send_get_request(self, endpoint):
        self.open_connection()
        request = f'GET {endpoint} HTTP/1.1\r\nHost:{self.host}:{self.port}\r\n\r\n'
        self.client.send(request.encode())

    def send_post_request(self, endpoint, data):
        self.open_connection()
        request = f'POST {endpoint} HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nContent-Type: application/json\r\nContent-Length: {len(str(data))}\r\n\r\n' + str(
            json.dumps(data))
        self.client.send(request.encode())

    def send_delete_request(self, endpoint):
        self.open_connection()
        request = f'DELETE {endpoint} HTTP/1.1\r\nHost:{self.host}:{self.port}\r\n\r\n'
        self.client.send(request.encode())

    def get_response(self):
        total_data = list()
        while True:
            data = self.client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break
        self.close_connection()
        return response_parser(total_data)

    def close_connection(self):
        self.client.close()