import json
from http.server import BaseHTTPRequestHandler, HTTPServer

items = [
    {"id": 1, "name": "item 1", "price": 5, "count": 32},
    {"id": 2, "name": "item 1", "price": 5, "count": 32}
]
item_tags = ["name", "price", "count"]
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/items':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(json.dumps(items).encode('utf-8'))
        elif self.path.startswith("/items/"):
            item_id = int(self.path.split("/")[-1])
            for i, item in enumerate(items):
                if item['id'] == item_id:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item).encode('utf-8'))
                    return
            self.send_response(404)
            self.end_headers()
            return
        else:
            self.send_error(404)

    def do_POST(self):
        endpoint = self.path.strip('/')

        if endpoint == 'items':
            # Get the request data and parse it as JSON
            data = self.rfile.read(int(self.headers.get('Content-Length')))
            json_data = json.loads(data)

            if len(data) == 0:
                self.send_response(204)
                self.end_headers()
                return

            dictionary_item = dict()
            dictionary = dict(json_data)
            dictionary_item["id"] = items[-1]["id"] + 1

            if item_tags[0] not in dictionary:
                self.send_response(403)
                self.end_headers()
                return
            for item in items:
                if dictionary[item_tags[0]] == item[item_tags[0]]:
                    self.send_response(409)
                    self.end_headers()
                    return
            for tag in item_tags:
                if tag in dictionary.keys():
                    dictionary_item[tag] = dictionary[tag]
                else:
                    self.send_response(403)
                    self.end_headers()
                    return
            items.append(dictionary_item)

            # Send a response with the processed data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(items[-1]).encode('utf-8'))

        else:
            self.send_error(404)

    def do_DELETE(self):
        if self.path.endswith("/items"):
            self.send_response(405)
            self.end_headers()
            return
        if self.path.startswith("/items/"):
            item_id = int(self.path.split("/")[-1])
            for i, item in enumerate(items):
                if item['id'] == item_id:
                    items.pop(i)
                    self.send_response(204)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    return
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(400)
        self.end_headers()
        return

    def do_PUT(self):
        if self.path.endswith("/items"):
            self.send_response(405)
            self.end_headers()
            return
        elif self.path.startswith("/items/"):
            item_id = int(self.path.split("/")[-1])
            content_length = int(self.headers['Content-Length'])
            if content_length.bit_length() == 0:
                self.send_response(204)
                self.end_headers()
                return
            item_data = json.loads(self.rfile.read(content_length))
            for item in items:
                if item['id'] == item_id:
                    dictionary = dict(item_data)
                    dict_iterator = dict(dictionary)
                    for key in dict_iterator.keys():
                        if key not in item_tags:
                            del dictionary[key]
                    item.update(dictionary)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item).encode('utf-8'))
                    return
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(400)
        self.end_headers()
        return


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server running at localhost:8000...')
    httpd.serve_forever()
