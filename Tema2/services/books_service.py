from services_controller.books_service_controller import Books_Service_Controller


class Books_Service:

    @staticmethod
    def get_all_books(self):
        response = Books_Service_Controller.get_all_books(self)
        info_response_message = dict()

        if response["status"] == 200:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}

            for item in range(0, len(response["message"])):
                books_dict = dict()
                books_dict["id"] = response["message"][item][0]
                books_dict["book_name"] = response["message"][item][1]
                books_dict["author_name"] = response["message"][item][2]
                books_dict["type_book"] = response["message"][item][3]
                info_response_message["message"]["book" + str(books_dict["id"])] = books_dict
        elif response["status"] == 404:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}

        return info_response_message

    @staticmethod
    def get_book_by_id(self, url_path):
        print(url_path)
        book_id = url_path.split('/')[-1]
        print(book_id)
        response = Books_Service_Controller.get_book_by_id(self, book_id)
        info_response_message = dict()
        book_dict = dict()

        if response["status"] == 200:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}

            book_dict["id"] = response["message"][0][0]
            book_dict["book_name"] = response["message"][0][1]
            book_dict["author_name"] = response["message"][0][2]
            book_dict["type_book"] = response["message"][0][3]
            info_response_message["message"] = book_dict
        elif response["status"] == 404:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}

        return info_response_message

    @staticmethod
    def get_author_of_book(self, url_path):
        print(url_path)
        book_id = url_path.split('/')[-2]

        print(book_id)
        response = Books_Service_Controller.get_author_of_book(self, book_id)

        info_response_message = dict()
        book_dict = dict()

        if response["status"] == 200:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}
            book_dict["author_name"] = response["message"][0][0]
            info_response_message["message"] = book_dict
        elif response["status"] == 404:
            info_response_message["status"] = response["status"]
            self.set_headers(info_response_message["status"])
            info_response_message["message"] = {}

        return info_response_message

    @staticmethod
    def post_book(self, book_info):
        response = Books_Service_Controller.post_book(self, book_info)
        self.set_headers(response["status"])

        return response

    @staticmethod
    def put_book(self, book_info):
        response = Books_Service_Controller.put_book(self, book_info)
        self.set_headers(response["status"])

        return response

    @staticmethod
    def delete_all_books(self):
        response = Books_Service_Controller.delete_all_books(self)
        info_response_message = dict()
        info_response_message["status"] = response["status"]
        self.set_headers(info_response_message["status"])

        return info_response_message

    @staticmethod
    def delete_book_by_id(self, url_path):
        book_id = url_path.split('/')[-1]
        response = Books_Service_Controller.delete_book_by_id(self, book_id)
        info_response_message = dict()
        info_response_message["status"] = response["status"]
        self.set_headers(info_response_message["status"])

        return info_response_message


