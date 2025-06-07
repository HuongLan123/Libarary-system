#Viết các chức năng : add_book, delete_book, search_book, update_book, sort_books
from cautrucdulieu import HashTable, merge_sort, print_wrapped_table
from test_condition import test_book
import csv
import sqlite3
def call_book_management():
    from menu import book_management
    book_management()
# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect("library11.db")
cursor = conn.cursor()
class Book:
    def __init__(self, isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity):
        self.isbn = isbn
        self.title = title
        self.genre = genre
        self.author = author
        self.added_quantity = added_quantity
        self.quantity = quantity
        self.available_quantity = available_quantity
        self.borrowed_quantity = borrowed_quantity
    def __str__(self):
        return f"{self.isbn} | {self.title} | {self.genre}| {self.author} | {self.added_quantity} | {self.quantity} | {self.available_quantity} | {self.borrowed_quantity}"

    def __eq__(self, other):
        return isinstance(other, Book) and self.isbn == other.isbn

    def __hash__(self):
        return hash(self.isbn)
book_table = HashTable()
headers = [
    "ISBN", "Tiêu đề", "Thể loại", "Tác giả",
    "SL nhập gần đây", "SL tổng", "SL còn", "SL đã mượn"
]
col_widths = [9, 25, 10, 10, 15, 15, 15, 10]
def key_choice(ch):
    if ch == "2":
        print("Chọn phương thức xóa sách:")
    elif ch == "3":
        print("Chọn phương thức tìm kiếm sách:")
    elif ch == "4":
        print("Chọn phương thức cập nhật sách:")
    elif ch == "5":
        print("Chọn phương thức sắp xếp sách:")
    print("1. Theo ISBN")
    print("2. Theo tiêu đề sách")
    print("3. Theo thể loại sách")
    print("4. Theo tác giả sách")
    key = input("Nhập lựa chọn của bạn (1-4): ").strip()
    if ch == "5":
        key_data = ""
        return key, key_data
    if key == "1":
        key_data = input("Nhập ISBN sách: ").strip()
    elif key == "2":
        key_data = input("Nhập tiêu đề sách: ").strip()
    elif key == "3":
        key_data = input("Nhập thể loại sách: ").strip()
    elif key == "4":
        key_data = input("Nhập tác giả sách: ").strip()
    else:
        print("Kết quả chọn không hợp lệ")
    return key, key_data
def book_choice():
    ch = input("Nhập lựa chọn của bạn: ")
    while True:
        if ch not in map(str, range(1, 8)):
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")
            continue
        if ch == "1":
            add_book()
        elif ch == "6":
            print("Danh sách các sách hiện tại")
            books = book_table.get_all_values()
            books_print = []
            for book in books:
                books_print.append(list(book.__dict__.values()))
            print_wrapped_table(headers, books_print, col_widths)
            call_book_management()
        elif ch == "7":
            print("Trở về menu chính.")
            from main import main
            main()
            break
        key, key_data = key_choice(ch)
        if ch == "2":
            if key == "3" or key == "4":
                print("Xóa sách theo thể loại và tác giả không được hỗ trợ.")
                print("Chọn lại cách xóa sách khác")
                continue
            else: 
                delete_book(key, key_data)
        elif ch == "3":
            search_book(key, key_data)
        elif ch == "4":
            if key == "3" or key == "4" or key == "2":
                print("Cập nhật sách theo tiêu đề, tác giả, thể loại không được hỗ trợ.")
                print("Chọn lại cách cập nhật sách")
                continue
            else: 
                update_book(key, key_data)
        elif ch == "5":
            sort_books(key)
        
def add_book_file():
    filename = input("Nhập tên file (VD: books.csv): ").strip()
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            books = csv.DictReader(csvfile)
            for row in books:
                isbn = row["ISBN"]
                title = row["Title"]
                genre = row["Genre"]
                author = row["Author"]
                added_quantity = int(row["Added Quantity"])
                quantity = int(row["Quantity"])
                available_quantity = int(row["Available"])
                borrowed_quantity = int(row["Borrowed Quantity"])
                is_valid, message = test_book(isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity)
                if is_valid:
                    book = Book(isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity)
                    if not book_table.search(isbn):
                        book_table.insert(isbn, book)
                        print(f"Thêm sách '{title}' thành công.")
                        cursor.execute("""
        INSERT INTO books (isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity))
                        conn.commit()
                    else:
                        print(f"Sách ISBN '{isbn}' đã tồn tại.")
                else:
                    print(f"Lỗi: {message}")
                    return
    except FileNotFoundError:
        print(f"Không tìm thấy file '{filename}'")
        return 
    except Exception as e:
        print(f"Lỗi khi thêm sách từ file: {e}")
        return
def add_book_terminal():
    isbn = input("Nhập ISBN: ").strip()
    title = input("Nhập tiêu đề sách: ").strip()
    genre = input("Nhập thể loại sách: ").strip()
    author = input("Nhập tác giả: ").strip()
    added_quantity = int(input("Nhập tổng số lượng sách lưu trữ: "))
    borrowed_quantity = input("Nhập số lượng sách đã được mượn (nếu sách đã tồn tại nhưng chưa đưa vào hệ thống, nếu chưa có thì để trống, mặc định là 0): ").strip()
    quantity = added_quantity
    if borrowed_quantity == "":
        borrowed_quantity = 0
    borrowed_quantity = int(borrowed_quantity)
    available_quantity = int(quantity - borrowed_quantity)
    is_valid, message = test_book(isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity)
    if is_valid:
        book = Book(isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity)
        if not book_table.search(isbn):
            book_table.insert(book.isbn,book)
            print(f"Sách '{title}' đã được thêm thành công.")
            cursor.execute("""
        INSERT INTO books (isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity))
            conn.commit()
        else:
            print(f"Sách với ISBN '{isbn}' đã lưu thất bại.")
            return
    else:
        print(f"Lỗi: {message}")
        return
def add_book():
    print("Chọn phương thức thêm sách:")
    print("1. Thêm sách từ file")
    print("2. Thêm sách từ bàn phím")
    print("3. Trở về menu chính")
    while True:
        choice = input("Nhập lựa chọn của bạn (1 - 3): ")
        if choice == "1":
            add_book_file()
        elif choice == "2":
            add_book_terminal()        
        elif choice == "3":
            call_book_management()
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")
def delete_book(key, key_data):
    if key == "1":  # Xóa theo ISBN
        isbn = key_data
        if book_table.search(isbn):
            book_table.delete(isbn)
            print(f"Sách với ISBN '{isbn}' đã được xóa.")
        else:
            print(f"Sách với ISBN '{isbn}' không tồn tại.")
    elif key == "2":  # Xóa theo tiêu đề sách
        title = key_data
        for book in book_table:
            if title.strip().lower() == book.title.lower():
                book_table.delete(title)
                print(f"Sách với tiêu đề '{title}' đã được xóa.")
                cursor.execute("DELETE FROM books WHERE title = ?", (title,))
                conn.commit()
            else:
                print(f"Sách với tiêu đề '{title}' không tồn tại.")
        call_book_management()
def search_book(key, key_data):
    keyword = key_data.strip().lower()
    result = []
    for book in book_table.get_all_values():
        if key == "1" and keyword in book.isbn.lower():
            result.append(list(book.__dict__.values()))
        elif key == "2" and keyword in book.title.lower():
            result.append(list(book.__dict__.values()))
        elif key == "3" and keyword in book.genre.lower():
            result.append(list(book.__dict__.values()))
        elif key == "4" and keyword in book.author.lower():
            result.append(list(book.__dict__.values()))
    if len(result) >= 1:
        print("\nKết quả tìm kiếm:")
        print_wrapped_table(headers, result, col_widths)
    else:
        print("Không tìm thấy sách nào.")
    call_book_management()
def update_book(key, key_data):
    book = book_table.search(key_data)
    if not book:
        print("Không tìm thấy sách để cập nhật.")
        return
    print("Thông tin sách hiện tại:")
    print_wrapped_table(headers, [list(book.__dict__.values())], col_widths)
    print("Nhập thông tin mới (để trống nếu không muốn thay đổi):")
    new_title = input(f"Tiêu đề [{book.title}]: ").strip() or book.title
    new_genre = input(f"Thể loại [{book.genre}]: ").strip() or book.genre
    new_author = input(f"Tác giả [{book.author}]: ").strip() or book.author
    new_added_quantity = input(f"Nhập thêm số lượng sách [{book.added_quantity}]: ").strip() or book.added_quantity
    new_borrowed_quantity = input(f"Số lượng sách đã mượn [{book.borrowed_quantity}]: ").strip() or book.borrowed_quantity
    is_valid, message = test_book(book.isbn, new_title, new_genre, new_author, int(new_added_quantity), book.quantity, book.available_quantity, int(new_borrowed_quantity))
    if is_valid:
        book.title = new_title
        book.genre = new_genre
        book.author = new_author
        book.added_quantity = int(new_added_quantity)
        book.borrowed_quantity = int(new_borrowed_quantity)
        book.quantity += book.added_quantity
        book.available_quantity = book.quantity - book.borrowed_quantity
        print("Cập nhật sách thành công.")
        book_table.insert(book.isbn, book)
        cursor.execute("""
        UPDATE books
        SET title = ?, genre = ?, author = ?, added_quantity = ?, quantity = ?, available_quantity = ?, borrowed_quantity = ?
        WHERE isbn = ?
    """, (book.title, book.genre, book.author, book.added_quantity, book.quantity, book.available_quantity, book.borrowed_quantity, book.isbn))
        conn.commit()
        call_book_management()
    else:
        print(f"Lỗi: {message}")
        return
def sort_books(key):
    books = book_table.get_all_values()
    reverse = input("Bạn muốn sắp xếp theo thứ tự tăng dần (True / False)?")
    if reverse.lower() == "true":
        reverse = False
    else:
        reverse = True
    if key == "1":
        key_func = lambda book: book.isbn
    elif key == "2" :
        key_func = lambda book: book.title.lower()
    elif key == "3":
        key_func = lambda book: book.genre.lower()
    elif key == "4":
        key_func = lambda book: book.author.lower()
    sorted_books = merge_sort(books, key_func, reverse)
    print("\nDanh sách sách sau khi sắp xếp:")
    books_print = []
    for book in sorted_books:
        books_print.append(list(book.__dict__.values()))
    print_wrapped_table(headers, books_print, col_widths)
    call_book_management()