from services_controller.bookstores_service_controller import Bookstore_Service_Controller


class Bookstore_Service:

    @staticmethod
    def get_all_bookstores(self):
        response = Bookstore_Service_Controller.get_all_bookstores(self)
        info_response_message = dict()

        info_response_message["status"] = response["status"]
        self.set_headers(info_response_message["status"])
        info_response_message["message"] = {}

        for item in range(0, len(response["message"])):
            books_dict = dict()
            books_dict["id"] = response["message"][item][0]
            books_dict["id_book"] = response["message"][item][1]
            books_dict["bookstore_name"] = response["message"][item][2]
            info_response_message["message"]["bookstore" + str(books_dict["id"])] = books_dict

        return info_response_message

    @staticmethod
    def get_bookstore_by_id(self, url_path):
        print(url_path)
        book_id = url_path.split('/')[-1]
        print(book_id)
        response = Bookstore_Service_Controller.get_bookstore_by_id(self, book_id)
        info_response_message = dict()
        book_dict = dict()

        print("intrabook")

        if response["status"] == 200:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}
            book_dict["id"] = response["message"][0][0]
            book_dict["id_book"] = response["message"][0][1]
            book_dict["bookstore_name"] = response["message"][0][2]
            info_response_message["message"] = book_dict
        elif response["status"] == 404:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}

        return info_response_message

    @staticmethod
    def get_book_of_bookstores(self, url_path):
        print(url_path)
        book_id = url_path.split('/')[-2]

        print(book_id)
        response = Bookstore_Service_Controller.get_book_of_bookstore(self, book_id)
        info_response_message = dict()

        if response["status"] == 200:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}
            info_response_message["message"]["book"] = response["message"][0]
        elif response["status"] == 404:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}

        return info_response_message

    @staticmethod
    def post_bookstore(self, book_info):
        response = Bookstore_Service_Controller.post_bookstore(self, book_info)
        self.set_headers(response["status"])

        return response

    @staticmethod
    def put_bookstore(self, book_info):
        response = Bookstore_Service_Controller.put_bookstore(self, book_info)
        print(response)
        self.set_headers(response["status"])

        return response


    @staticmethod
    def delete_all_bookstores(self):
        response = Bookstore_Service_Controller.delete_all_bookstores(self)
        info_response_message = dict()
        info_response_message["status"] = response["status"]
        self.set_headers(info_response_message["status"])

        return info_response_message

    @staticmethod
    def delete_bookstore_by_id(self, url_path):
        book_id = url_path.split('/')[-1]
        response = Bookstore_Service_Controller.delete_bookstore_by_id(self, book_id)
        info_response_message = dict()
        info_response_message["status"] = response["status"]
        self.set_headers(info_response_message["status"])

        return info_response_message