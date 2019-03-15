from database import database

class Books_Service_Controller:

    def get_all_books(self):
        database_query = 'get_all_books'
        database_response = database.get_all_entities(database_query)

        if database_response["status"] != 200:
            return database_response

        return database_response

    def get_book_by_id(self, book_id):
        database_query = 'get_book_by_id'
        database_response = database.get_entity_by_id(database_query, book_id)

        if database_response['status'] != 200:
            return database_response

        return database_response

    def get_author_of_book(self, book_id):
        database_query = 'get_author_of_book'
        database_response = database.get_entity_by_id(database_query, book_id)

        if database_response['status'] != 200:
            return database_response

        return database_response

    def post_book(self, book_info):
        database_query = 'insert_book'
        print (book_info)
        database_response = database.post_entity(database_query, book_info)

        return database_response

    def put_book(self, book_info):
        database_query = 'update_book_by_id'
        database_response = database.put_entity_by_id(database_query, book_info)

        return database_response

    def delete_all_books(self):
        database_query = 'delete_all_books'
        database_response = database.delete_all_entities(database_query)

        return database_response

    def delete_book_by_id(self, book_id):
        database_query = 'delete_book_by_id'
        database_response = database.delete_entity_by_id(database_query, book_id)

        return database_response