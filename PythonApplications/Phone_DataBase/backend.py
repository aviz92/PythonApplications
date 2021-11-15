import sqlite3


class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS book ("
                         "id INTEGER PRIMARY KEY, title text, author text, date integer, serial_number integer)")
        self.conn.commit()

    def insert(self, title, author, date, serial_number):
        self.cur.execute("INSERT INTO book VALUES (NULL,?,?,?,?)", (title, author, date, serial_number))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM book")
        rows = self.cur.fetchall()
        return rows

    def search(self, title="", author="", date="", serial_number=""):
        # self.cur.execute("SELECT * FROM book WHERE title=? OR author=? OR date=? OR serial_number=?",
        #                  (title, author, date, serial_number))
        self.cur.execute(
            "SELECT * FROM book WHERE title like (?) AND author like (?) AND date like (?) AND serial_number like (?)",
            ("%" + title + "%", "%" + author + "%", "%" + date + "%", "%" + serial_number + "%"))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id_parameter):
        self.cur.execute("DELETE FROM book WHERE id=?", (id_parameter,))
        self.conn.commit()

    def update(self, id_parameter, title, author, date, serial_number):
        self.cur.execute("UPDATE book SET title=?, author=?, date=?, serial_number=? WHERE id=?",
                         (title, author, date, serial_number, id_parameter))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
