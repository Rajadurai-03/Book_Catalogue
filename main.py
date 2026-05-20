import mysql.connector

def initialize_db(cursor, connection):
    cursor.execute("CREATE DATABASE IF NOT EXISTS books")
    cursor.execute("USE books")
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        username VARCHAR(30) PRIMARY KEY,
                        password VARCHAR(20), 
                        doj DATE,
                        role VARCHAR(10) DEFAULT 'user',
                        reset_requested BOOLEAN DEFAULT FALSE)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS books_read(
                        username VARCHAR(30), 
                        book_name VARCHAR(100), 
                        author VARCHAR(100),
                        chapters INT, 
                        chapters_read INT, 
                        rating INT,
                        PRIMARY KEY (username, book_name))''')

    try: cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(10) DEFAULT 'user'")
    except mysql.connector.errors.ProgrammingError: pass
    try: cursor.execute("ALTER TABLE users ADD COLUMN reset_requested BOOLEAN DEFAULT FALSE")
    except mysql.connector.errors.ProgrammingError: pass
    try: cursor.execute("ALTER TABLE books_read ADD COLUMN author VARCHAR(100) DEFAULT 'Unknown'")
    except mysql.connector.errors.ProgrammingError: pass
    
    cursor.execute("SELECT * FROM users WHERE username = 'Raja'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, doj, role) VALUES ('Raja', 'Raj@1234', CURRENT_DATE(), 'admin')")
    connection.commit()

def dbsignup(cursor, name, password):
    query = "INSERT INTO users (username, password, doj) VALUES (%s, %s, CURRENT_DATE())"
    cursor.execute(query, (name, password))

def dbsignin(cursor, name, password):
    query = "SELECT password, role FROM users WHERE username = %s"
    cursor.execute(query, (name,))
    row = cursor.fetchone()
    if row is None: return False, None
    if password == row[0]: return True, row[1]
    return False, None

def request_password_reset(cursor, username):
    query = "UPDATE users SET reset_requested = TRUE WHERE username = %s"
    cursor.execute(query, (username,))

def approve_reset(cursor, username):
    temp_pass = f"{username}@123"
    cursor.execute("UPDATE users SET password = %s, reset_requested = FALSE WHERE username = %s", (temp_pass, username))

def dbupdatepassword(cursor, username, new_password):
    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))

def dbview(cursor, name):
    query = "SELECT username, book_name, chapters, chapters_read, rating, author FROM books_read WHERE username = %s"
    cursor.execute(query, (name,))
    return cursor.fetchall()

def dbaddbook(cursor, name, book_name, author, chapters, chapters_read, rating):
    query = "INSERT INTO books_read (username, book_name, author, chapters, chapters_read, rating) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (name, book_name, author, chapters, chapters_read, rating))

def dbdeletebook(cursor, name, book_name):
    query = "DELETE FROM books_read WHERE username = %s AND book_name = %s"
    cursor.execute(query, (name, book_name))

def dbupdateprogress(cursor, name, book_name, new_chapter):
    query = "UPDATE books_read SET chapters_read = %s WHERE username = %s AND book_name = %s"
    cursor.execute(query, (new_chapter, name, book_name))

def get_user_rank(cursor, username):
    query = """
        SELECT username, SUM(chapters_read / chapters) + COUNT(book_name) as score
        FROM books_read GROUP BY username ORDER BY score DESC
    """
    cursor.execute(query)
    rankings = cursor.fetchall()
    for index, user in enumerate(rankings):
        if user[0] == username: return index + 1 
    return 0 

def get_all_users(cursor):
    cursor.execute("SELECT username, doj, reset_requested FROM users WHERE role != 'admin'")
    return cursor.fetchall()

def delete_user(cursor, username):
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    cursor.execute("DELETE FROM books_read WHERE username = %s", (username,))