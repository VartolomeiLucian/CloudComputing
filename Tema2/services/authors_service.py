from services_controller.authors_service_controller import Authors_Service_Controller
from urllib.parse import urlparse

class Authors_Service:

    @staticmethod
    def get_all_authors(self):
        response = Authors_Service_Controller.get_all_authors(self)
        info_response_message = dict()

        info_response_message["status"] = response["status"]
        self.set_headers(info_response_message["status"])
        info_response_message["message"] = {}

        for item in range(0, len(response["message"])):
            books_dict = dict()
            books_dict["id"] = response["message"][item][0]
            books_dict["id_book"] = response["message"][item][1]
            books_dict["author_name"] = response["message"][item][2]
            info_response_message["message"]["author" + str(books_dict["id"])] = books_dict

        return info_response_message

    @staticmethod
    def get_author_by_id(self, url_path):
        print(url_path)
        author_id = url_path.split('/')[-1]
        print(author_id)
        response = Authors_Service_Controller.get_author_by_id(self, author_id)
        info_response_message = dict()
        author_dict = dict()

        if response["status"] == 200:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}

            author_dict["id"] = response["message"][0][0]
            author_dict["id_book"] = response["message"][0][1]
            author_dict["author_name"] = response["message"][0][2]
            info_response_message["message"] = author_dict
        elif response["status"] == 404:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}

        return info_response_message

    @staticmethod
    def get_book_of_author(self, server_request):
        url_path = urlparse(server_request.path).path
        book_id = (url_path.split('/')[-2])

        return Authors_Service_Controller.get_author_by_id(self, book_id)


    @staticmethod
    def post_author(self, book_info):
        response = Authors_Service_Controller.post_author(self, book_info)
        self.set_headers(response["status"])

        return response

    @staticmethod
    def put_author(self, book_info):
        response = Authors_Service_Controller.put_author(self, book_info)
        self.set_headers(response["status"])

        return response

    @staticmethod
    def delete_all_authors(self):
        response = Authors_Service_Controller.delete_all_authors(self)
        info_response_message = dict()
        info_response_message["status"] = response["status"]
        self.set_headers(info_response_message["status"])

        return info_response_message

    @staticmethod
    def delete_author_by_id(self, url_path):
        author_id = url_path.split('/')[-1]
        response = Authors_Service_Controller.delete_author_by_id(self, author_id)
        info_response_message = dict()
        info_response_message["status"] = response["status"]
        self.set_headers(info_response_message["status"])

        return info_response_message