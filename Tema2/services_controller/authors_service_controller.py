from database import database

class Authors_Service_Controller:

    def get_all_authors(self):
        database_query = 'get_all_authors'
        database_response = database.get_all_entities(database_query)

        if database_response["status"] != 200:
            return database_response["status"]

        return database_response

    def get_author_by_id(self, book_id):
        database_query = 'get_author_by_id'
        database_response = database.get_entity_by_id(database_query, book_id)

        if database_response['status'] != 200:
            return database_response

        return database_response

    def get_book_of_author(self, book_id):
        database_query = 'get_book_of_author'
        database_response = database.get_entity_by_id(database_query, book_id)

        if database_response != 200:
            return database_response["status"]

        database_response['type'] = {'type' : database_response['type']}
        database_response['message'] = {'author': database_response['message']}

        return database_response

    def post_author(self, author_info):
        database_query = 'insert_author'
        print (author_info)
        database_response = database.post_entity(database_query, author_info)

        return database_response

    def put_author(self, book_info):
        database_query = 'update_author_by_id'
        database_response = database.put_entity_by_id(database_query, book_info)

        return database_response

    def delete_all_authors(self):
        database_query = 'delete_all_authors'
        database_response = database.delete_all_entities(database_query)

        return database_response

    def delete_authors_by_id(self, book_id):
        database_query = 'delete_authors_by_id'
        database_response = database.delete_entity_by_id(database_query, book_id)

        return database_response

    def delete_author_by_id(self, book_id):
        database_query = 'delete_author_by_id'
        database_response = database.delete_entity_by_id(database_query, book_id)

        return database_response
