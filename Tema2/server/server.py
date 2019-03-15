from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from database import database
from urllib.parse import urlparse
from services.books_service import Books_Service_Controller
from services.authors_service import Authors_Service_Controller
from services.bookstore_service import Bookstore_Service_Controller
from socketserver import ThreadingMixIn
import re

PORT = 8081


class My_Request_Handler(BaseHTTPRequestHandler):

    # BOOKS

    def set_headers(self, response):
        self.send_response(response)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def get_all_books_service_response(self):
        response_request = Books_Service_Controller.get_all_books(self)
        json_string = json.dumps(response_request).encode()
        self.wfile.write("\n".encode())
        self.wfile.write(json_string)
        self.wfile.write("\n".encode())

    def get_book_by_id(self, url_path):
        response_request = Books_Service_Controller.get_book_by_id(self, url_path)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)

    def get_author_of_book(self, url_path):
        response = Books_Service_Controller.get_author_of_book(self, url_path)
        json_string = json.dumps(response).encode()
        self.wfile.write(json_string)

    def post_book(self):

        post_book_info = []
        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)

        try:
            json_data = json.loads(post_data)
            print(json_data)
        except:
            json_data = dict()

        post_book_info.append(json_data["book_name"])
        post_book_info.append(json_data["author_name"])
        post_book_info.append(json_data["book_type"])

        response_request = Books_Service_Controller.post_book(self, post_book_info)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)


    def put_book(self, url_path):
        put_book_info = []
        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)

        try:
            json_data = json.loads(post_data)
            print(json_data)
        except:
            json_data = dict()

        put_book_info.append(json_data["book_name"])
        put_book_info.append(json_data["author_name"])
        put_book_info.append(json_data["book_type"])
        book_id = url_path.split('/')[-1]
        put_book_info.append(book_id)

        print(put_book_info)

        response_request = Books_Service_Controller.put_book(self, put_book_info)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)


    def delete_all_books(self):
        response_request = Books_Service_Controller.delete_all_books(self)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)

    def delete_book_by_id(self, url_path):
        response_request = Books_Service_Controller.delete_book_by_id(self, url_path)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)



    # AUTHORS

    def get_all_authors_service_response(self):
        response = Authors_Service_Controller.get_all_authors(self)
        json_string = json.dumps(response).encode()
        self.wfile.write("\n".encode())
        self.wfile.write(json_string)
        self.wfile.write("\n".encode())


    def get_author_by_id(self, url_path):
        response_request = Authors_Service_Controller.get_author_by_id(self, url_path)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)

    def post_author(self):

        post_author_info = []
        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)

        try:
            json_data = json.loads(post_data)
            print(json_data)
        except:
            json_data = dict()

        post_author_info.append(json_data["id_book"])
        post_author_info.append(json_data["author_name"])

        response = Authors_Service_Controller.post_author(self, post_author_info)
        json_string = json.dumps(response).encode()
        self.wfile.write(json_string)

    def put_author(self, url_path):
        put_author_info = []
        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)

        try:
            json_data = json.loads(post_data)
            print(json_data)
        except:
            json_data = dict()

        put_author_info.append(json_data["id_book"])
        put_author_info.append(json_data["author_name"])
        author_id = url_path.split('/')[-1]
        put_author_info.append(author_id)

        print(put_author_info)

        response_request = Authors_Service_Controller.put_author(self, put_author_info)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)

    def delete_all_authors(self):
        response_request = Authors_Service_Controller.delete_all_authors(self)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)

    def delete_author_by_id(self, url_path):
        response_request = Authors_Service_Controller.delete_author_by_id(self, url_path)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)

    # BOOKSTORES

    def get_all_bookstores_service_response(self):
        response = Bookstore_Service_Controller.get_all_bookstores(self)
        json_string = json.dumps(response).encode()
        self.wfile.write("\n".encode())
        self.wfile.write(json_string)
        self.wfile.write("\n".encode())

    def get_bookstore_by_id(self, url_path):
        response_request = Bookstore_Service_Controller.get_bookstore_by_id(self, url_path)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)

    def get_book_of_bookstores(self, url_path):
        response = Bookstore_Service_Controller.get_book_of_bookstores(self, url_path)
        json_string = json.dumps(response).encode()
        self.wfile.write(json_string)

    def post_bookstore(self):

        post_book_info = []
        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)

        try:
            json_data = json.loads(post_data)
            print(json_data)
        except:
            json_data = dict()

        post_book_info.append(json_data["id_book"])
        post_book_info.append(json_data["bookstore_name"])

        response_request = Bookstore_Service_Controller.post_bookstore(self, post_book_info)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)

    def put_bookstore(self, url_path):
        put_bookstore_info = []
        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)

        try:
            json_data = json.loads(post_data)
            print(json_data)
        except:
            json_data = dict()

        put_bookstore_info.append(json_data["id_book"])
        put_bookstore_info.append(json_data["bookstore_name"])
        bookstore_id = url_path.split('/')[-1]
        put_bookstore_info.append(bookstore_id)

        print(put_bookstore_info)

        response_request = Bookstore_Service_Controller.put_bookstore(self, put_bookstore_info)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)

    def delete_all_bookstores(self):
        response_request = Bookstore_Service_Controller.delete_all_bookstores(self)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)

    def delete_bookstore_by_id(self, url_path):
        response_request = Bookstore_Service_Controller.delete_bookstore_by_id(self, url_path)
        json_string = json.dumps(response_request).encode()
        self.wfile.write(json_string)


    def do_GET(self):

        url_path = urlparse(self.path).path

        try:
            if re.search('^/books$', url_path):
                self.get_all_books_service_response()
                return
            if re.search('^/books/\d+?$', url_path):
                self.get_book_by_id(url_path)
                return
            if re.search('^/books/\d+?/authors$', url_path):
                self.get_author_of_book(url_path)
                return
            if re.search('^/authors$', url_path):
                self.get_all_authors_service_response()
                return
            if re.search('^/authors/\d+?$', url_path):
                self.get_author_by_id(url_path)
                return
            if re.search('^/bookstores$', url_path):
                self.get_all_bookstores_service_response()
                return
            if re.search('^/bookstores/\d+?$', url_path):
                self.get_bookstore_by_id(url_path)
                return
            if re.search('^/bookstores/\d+?/books$', url_path):
                self.get_book_of_bookstores(url_path)
                return

        except Exception as e:
            print(e)

    def do_POST(self):

        url_path = urlparse(self.path).path

        try:

            if self.headers['Content-Type'] != 'application/json':
                status = dict()
                status["status"] = 415
                self.set_headers(status["status"])
                json_string = json.dumps(status).encode()
                self.wfile.write(json_string)
                return

            if re.search('^/books$', url_path):
                self.post_book()
                return
            if re.search('^/authors$', url_path):
                self.post_author()
                return
            if re.search('^/bookstores$', url_path):
                self.post_bookstore()
                return

        except Exception as e:
            print(e)

    def do_PUT(self):

        url_path = urlparse(self.path).path

        try:
            if self.headers['Content-Type'] != 'application/json':
                status = dict()
                status["status"] = 415
                self.set_headers(status["status"])
                json_string = json.dumps(status).encode()
                self.wfile.write(json_string)
                return

            if self.headers['Content-Type'] != 'application/json':
                status = dict()
                status["status"] = 415
                self.set_headers(status["status"])
                json_string = json.dumps(status).encode()
                self.wfile.write(json_string)
                return

            if re.search('^/books/\d+?$', url_path):
                self.put_book(url_path)
                return
            if re.search('^/authors/\d+?$', url_path):
                self.put_author(url_path)
                return
            if re.search('^/bookstores/\d+?$', url_path):
                self.put_bookstore(url_path)
                return

        except Exception as e:
            print(e)

    def do_DELETE(self):

        url_path = urlparse(self.path).path

        try:
            if re.search('^/books$', url_path):
                self.delete_all_books()
                return
            if re.search('^/books/\d+?$', url_path):
                self.delete_book_by_id(url_path)
                return
            if re.search('^/authors$', url_path):
                self.delete_all_authors()
                return
            if re.search('^/authors/\d+?$', url_path):
                self.delete_author_by_id(url_path)
                return
            if re.search('^/bookstores$', url_path):
                self.delete_all_bookstores()
                return
            if re.search('^/bookstores/\d+?$', url_path):
                self.delete_bookstore_by_id(url_path)
                return


        except Exception as e:
            print (e)


class TreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run_server(server, handler):
    print('HTTP Server is starting...')
    server_addr = ('127.0.0.1', PORT)
    httpd = server(server_addr, handler)
    print('HTTP Server listening on PORT:', PORT)
    print('HTTP Server is running!')
    httpd.serve_forever()


if __name__ == "__main__":
    database.initialisation_database()
    book_info1 = ('Carte2', 'Autor2', 'tip2')
    book_info2 = ('Carte3', 'Autor2', 'tip2')
    book_info3 = ('Carte4', 'Autor5', 'tip2')
    author1 = (1, "Autor1")
    author2 = (1, "Autor2", 1)
    bookstore1 = ('1', 'bookstore1')
    bookstore2 = ('2', 'bookstore1')
    print(database.post_entity('insert_book', book_info1))
    print(database.post_entity('insert_book', book_info2))
    print(database.post_entity('insert_book', book_info3))
    print(database.post_entity('insert_author', author1))
    print(database.post_entity('insert_author', author2))
    print(database.post_entity('insert_bookstore', bookstore1))
    print(database.post_entity('insert_bookstore', bookstore2))
    database.view_tables()
    print(database.put_entity_by_id('update_author_by_id', author2))
    database.view_tables()
    print(database.get_entity_by_id('get_author_of_book', 1))
    # database.view_tables()
    run_server(TreadingHTTPServer, My_Request_Handler)


    # # # database.execute_query()
    # database.view_tables()
    # # # print(database.get_all_entities('get_all_bookstores'))
    # # # print(database.get_entity_by_id('get_book_by_id', '2'))
    # book_info1 = ('Carte2', 'Autor2', 'tip2')
    # # book_info2 = ('Carte3', 'Autor2', 'tip2')
    # print(database.post_entity('insert_book', book_info1))
    # database.view_tables()
    # # # print(database.delete_all_entities('delete_all_authors'))
    # # print(database.put_entity_by_id('update_book_by_id', book_info2))
    # # database.view_tables()
    # # print(database.delete_entity_by_id('delete_book_by_id', '1'))
    # # database.view_tables()
