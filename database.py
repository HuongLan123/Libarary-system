import sqlite3
from book import book_table, Book
from reader import reader_table, Reader
from loan import LoanRecord, LoanManager
from cautrucdulieu import HashTable, LinkedListForHash, BSTree
def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn,cursor
conn, cursor = create_connection("library11.db")
# Tạo bảng nếu chưa tồn tại
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
    isbn TEXT PRIMARY KEY,
    title TEXT,
    genre TEXT,           
    author TEXT,
    added_quantity INTEGER,
    quantity INTEGER DEFAULT 0,
    available_quantity INTEGER,
    borrowed_quantity INTEGER DEFAULT 0
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS readers (
    MSSV TEXT PRIMARY KEY,
    name TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reader_id TEXT,
    isbn TEXT,
    borrow_date TEXT,
    due_date TEXT,
    return_date TEXT,
    status TEXT
)''')

conn.commit()
def reload_database_book():
    global conn, cursor
    if conn:
        # Xóa toàn bộ dữ liệu trong bảng băm
        for i in range(book_table.capacity):
            book_table.table[i] = LinkedListForHash()
        book_table.size = 0
        cur = conn.cursor()
        # Truy vấn lại dữ liệu từ SQLite và chèn vào bảng băm
        for row in cursor.execute("SELECT * FROM books"):
            book = Book(*row[:8])
            book.available_quantity = row[6]
            book.borrowed_quantity = row[7]
            book.quantity = row[5]
            book_table.insert(book.isbn, book)
def reload_database_reader():
    cursor = conn.cursor()
    for i in range(reader_table.capacity):
        reader_table.table[i] = LinkedListForHash()
    reader_table.size = 0
    for row in cursor.execute("SELECT * FROM readers"):
        reader_id, name = row
        from reader import Reader
        reader_table.insert(reader_id, Reader(reader_id, name))
loan_manager = LoanManager(conn)
def reload_database_loan(loan_manager):
    global conn, cursor
    loan_manager = LoanManager(conn)
    if loan_manager.conn:
        loan_manager.tree = BSTree()
        cursor = loan_manager.conn.cursor()
        cursor.execute("SELECT * FROM loans")
        for row in cursor.fetchall():
            loan = LoanRecord(*row)
            loan_manager.tree.insert(loan.loan_id, loan)
