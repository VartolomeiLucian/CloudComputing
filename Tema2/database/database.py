import sqlite3

DATABASE = "database1"

create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                            id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            book_name text NOT NULL,
                            author_name text NOT NULL,
                            book_type text NOT NULL,
                            UNIQUE (book_name)
                        );"""

create_authors_table = """CREATE TABLE IF NOT EXISTS authors (
                            id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            id_book integer NOT NULL,
                            author_name text NOT NULL,
                            FOREIGN KEY (id_book) REFERENCES books(id)
                            UNIQUE (id_book)
                            );"""

create_bookstore_table = """CREATE TABLE IF NOT EXISTS bookstores (
                                id integer PRIMARY KEY AUTOINCREMENT NOT NULL ,
                                id_book integer NOT NULL,
                                bookstore_name text NOT NULL,
                                FOREIGN KEY (id_book) REFERENCES books(id) 
                                UNIQUE (id_book)
                                );"""

drop_books_table = "DROP TABLE books"
drop_authors_table = "DROP TABLE authors"
drop_bookstore_table = "DROP TABLE bookstores"

insert_book = "INSERT INTO books(book_name, author_name, book_type) VALUES (?, ?, ?)"
insert_author = "INSERT INTO authors(id_book, author_name) VALUES (?, ?)"
insert_bookstore = "INSERT INTO bookstores(id_book, bookstore_name) VALUES (?, ?)"

insert_book_id = "INSERT INTO books(id, book_name, author_name, book_type) VALUES (?, ?, ?, ?)"
insert_author_id = "INSERT INTO authors(id, id_book, author_name) VALUES (?, ?, ?)"
insert_bookstore_id = "INSERT INTO bookstores(id, id_book, bookstore_name) VALUES (?, ?, ?)"

get_all_books = "SELECT * FROM books"
get_all_authors = "SELECT * FROM authors"
get_all_bookstores = "SELECT * FROM bookstores"

get_book_by_id = "SELECT * FROM books WHERE id=?"
get_author_by_id = "SELECT * FROM authors WHERE id = ?"
get_bookstore_by_id = "SELECT * FROM bookstores WHERE id = ?"

get_books_of_author = """SELECT B.id, B.book_name, B.author_name, B.book_type
                         FROM books AS B JOIN authors AS A ON B.id = A.id_book
                         WHERE A.author_name = ?"""

get_author_of_book = """SELECT A.author_name FROM authors as A 
                        JOIN books as B ON A.id_book = B.id
                        WHERE B.id = ?"""

get_book_of_bookstore = """SELECT B.book_name, B.author_name, B.book_type FROM books as B 
                        JOIN bookstores as BS ON B.id = BS.id_book
                        WHERE BS.id_book = ?"""

update_book_by_id = "UPDATE books SET book_name = ?, author_name = ?, book_type = ? WHERE id = ?"
update_author_by_id = "UPDATE authors SET id_book = ?, author_name = ? WHERE id = ?"
update_bookstore_by_id = "UPDATE bookstores SET id_book = ?, bookstore_name = ? WHERE id = ?"


delete_book_by_id = "DELETE FROM books WHERE id=?"
delete_author_by_id = "DELETE FROM authors WHERE id = ?"
delete_bookstore_by_id = "DELETE FROM bookstores WHERE id = ?"


delete_all_books = "DELETE FROM books"
delete_all_authors = "DELETE FROM authors"
delete_all_bookstores = "DELETE FROM bookstores"

def create_connection():
    try:
        connection = sqlite3.connect(DATABASE)
        return connection
    except Exception as e:
        print(e)

def create_table(create_table_sql):
    connection = create_connection()
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
        connection.commit()
    except Exception as e:
        print(e)

def drop_table(drop_table_sql):
    connection = create_connection()
    try:
        c = connection.cursor()
        c.execute(drop_table_sql)
        connection.commit()

        c.close()
        connection.close()
    except Exception as e:
        print(e)

def initialisation_database():
    try:
        drop_table(drop_books_table)
        drop_table(drop_authors_table)
        drop_table(drop_bookstore_table)

        create_table(create_books_table)
        create_table(create_authors_table)
        create_table(create_bookstore_table)

    except Exception as e:
        print(e)



def insert_books(book_name, author_name, book_type):
    connection = create_connection()
    curs = connection.cursor()
    data = (book_name, author_name, book_type)

    curs.execute(insert_book, data)
    connection.commit()

def insert_authors(id_book, author_name):
    connection = create_connection()
    curs = connection.cursor()
    data = (id_book, author_name)

    curs.execute(insert_author, data)
    connection.commit()

def insert_bookstores(id_book, bookstore_name):
    connection = create_connection()
    curs = connection.cursor()
    data = (id_book, bookstore_name)

    curs.execute(insert_bookstore, data)
    connection.commit()

    return curs.lastrowid

def view_tables():
    connection = create_connection()
    curs = connection.cursor()

    for row in curs.execute(get_all_books):
        print(row)

    for row in curs.execute(get_all_authors):
        print(row)

    for row in curs.execute(get_all_bookstores):
        print(row)

def execute_query():
    conn = create_connection()
    if conn is not None:
        create_table(create_books_table)
        create_table(create_authors_table)
        create_table(create_bookstore_table)
        insert_books('Ion', 'LiviuRebreanu', 'Roman')
        insert_authors(11, "LiviuRebreanu")
        insert_bookstores(1, "Carturesti")
    else:
        print("Error! Cannot create the database connection!")

def get_all_entities(query):
    connection = create_connection()
    info = dict()

    if query == 'get_all_books':
        query = get_all_books
    elif query == 'get_all_authors':
        query = get_all_authors
    elif query == 'get_all_bookstores':
        query = get_all_bookstores

    try:
        cursor = connection.cursor()
        entities = []

        for row in cursor.execute(query):
            entities.append(row)

        cursor.close()
        connection.close()
    except Exception as e:
        return e

    # No Content
    if len(entities) == 0:
        info['status'] = 404
        return info

    info["status"] = 200
    info["type"] = 'application/json'
    info["message"] = entities

    return info

def get_entity_by_id(query, id):
    connection = create_connection()
    info = dict()
    no_content = False

    if query == 'get_book_by_id':
        query = get_book_by_id
    elif query == 'get_author_by_id':
        query = get_author_by_id
    elif query == 'get_bookstore_by_id':
        query = get_bookstore_by_id
    elif query == 'get_author_of_book':
        query = get_author_of_book
    elif query == 'get_book_of_bookstore':
        query = get_book_of_bookstore

    try:
        cursor = connection.cursor()
        entities = []
        print(id)
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        info1 = dict()
        if row is None:
            print("None")
            info1['status'] = 404
            info['type'] = 'application/json'
            info['message'] = entities
            print(info1)
            return info1

        entities.append(row)
        cursor.close()
        connection.close()
    except Exception as e:
        return e

    # No Content
    if no_content is True:
        info['status'] = 204
        return info

    info['status'] = 200
    info['type'] = 'application/json'
    info['message'] = entities

    return info

def post_entity(query, data):
    connection = create_connection()
    info = dict()
    print(data)

    if query == 'insert_book':
        query = insert_book
    elif query == 'insert_book_id':
        query = insert_book_id
    elif query == 'insert_author':
        query = insert_author
    elif query == 'insert_author_id':
        query = insert_author_id
    elif query == 'insert_bookstore':
        query = insert_bookstore
    elif query == 'insert_bookstore_id':
        query = insert_bookstore_id

    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()

    # trebuie sa adaug status code pentru fail
    except Exception as e:
        if str(e).find("UNIQUE") != -1:
            # Conflict
            info["status"] = 409
        else:
            # Not Found
            info["status"] = 404
        print(e)
        return info

    info["status"] = 201
    return info

def put_entity_by_id(query, data):
    connection = create_connection()
    info = dict()
    print(data)

    if query == 'update_book_by_id':
        query = update_book_by_id
    elif query == 'update_author_by_id':
        query = update_author_by_id
    elif query == 'update_bookstore_by_id':
        query = update_bookstore_by_id

    try:
        cursor = connection.cursor()
        cursor.execute(query, data)

        if cursor.rowcount == 0:
            # Not Found
            info["status"] = 404
            return info
        
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        return e

    info['status'] = 200
    return info

def delete_all_entities(query):
    connection = create_connection()
    info = dict()

    if query == 'delete_all_books':
        query = delete_all_books
    elif query == 'delete_all_authors':
        query = delete_all_authors
    elif query == 'delete_all_bookstores':
        query = delete_all_bookstores

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        if cursor.rowcount == 0:
            # Not Found
            info["status"] = 404
            return info

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        return e

    info["status"] = 200
    return info


def delete_entity_by_id(query, id):
    connection = create_connection()
    info = dict()

    if query == 'delete_book_by_id':
        query = delete_book_by_id
    elif query == 'delete_author_by_id':
        query = delete_author_by_id
    elif query == 'delete_bookstore_by_id':
        query = delete_bookstore_by_id

    try:
        cursor = connection.cursor()
        print(id)
        cursor.execute(query, id)

        if cursor.rowcount == 0:
            # Not Found
            info["status"] = 404
            return info

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        return e

    info['status'] = 200
    return info
