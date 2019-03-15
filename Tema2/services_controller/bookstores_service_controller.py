from database import database

class Bookstore_Service_Controller:

    def get_all_bookstores(self):
        database_query = 'get_all_bookstores'
        database_response = database.get_all_entities(database_query)

        if database_response["status"] != 200:
            return database_response["status"]

        return database_response

    def get_bookstore_by_id(self, book_id):
        database_query = 'get_bookstore_by_id'
        database_response = database.get_entity_by_id(database_query, book_id)

        print(database_response)
        if database_response['status'] != 200:
            return database_response

        return database_response

    def get_book_of_bookstore(self, book_id):
        database_query = 'get_book_of_bookstore'
        database_response = database.get_entity_by_id(database_query, book_id)

        if database_response["status"] != 200:
            return database_response

        return database_response

    def post_bookstore(self, book_info):
        database_query = 'insert_bookstore'
        # print (book_info)
        database_response = database.post_entity(database_query, book_info)

        return database_response

    def put_bookstore(self, book_info):
        database_query = 'update_bookstore_by_id'
        database_response = database.put_entity_by_id(database_query, book_info)

        return database_response

    def delete_all_bookstores(self):
        database_query = 'delete_all_bookstores'
        database_response = database.delete_all_entities(database_query)

        return database_response

    def delete_bookstore_by_id(self, book_id):
        database_query = 'delete_bookstore_by_id'
        database_response = database.delete_entity_by_id(database_query, book_id)

        return database_response