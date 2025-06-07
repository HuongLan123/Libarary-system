# loan.py
from cautrucdulieu import BSTree
from datetime import datetime, timedelta
import sqlite3

conn = sqlite3.connect("library11.db")
def call_loan_management():
    from menu import loan_management
    loan_management()
class LoanRecord:
    def __init__(self, loan_id, reader_id, isbn, borrow_date, due_date, return_date=None, status="Đang mượn"):
        self.loan_id = loan_id
        self.reader_id = reader_id
        self.isbn = isbn
        self.borrow_date = borrow_date if isinstance(borrow_date, datetime) else datetime.strptime(borrow_date, "%Y-%m-%d %H:%M:%S.%f")
        self.due_date = due_date if isinstance(due_date, datetime) else datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S.%f")
        self.return_date = return_date if isinstance(return_date, datetime) else (datetime.strptime(return_date, "%Y-%m-%d %H:%M:%S.%f") if return_date else None)
        self.status = status

    def __str__(self):
        return (f"[Loan ID: {self.loan_id}] Reader: {self.reader_id}, ISBN: {self.isbn}, "
                f"Borrowed: {self.borrow_date.date()}, Due: {self.due_date.date()}, "
                f"Returned: {self.return_date.date() if self.return_date else 'N/A'}, Status: {self.status}")

class LoanManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.tree = BSTree()
        self.book_cache = {}     # isbn -> available_quantity
        self.reader_cache = set()  # reader_id set
        self.load_all_data()

    def load_all_data(self):
        self.reader_cache.clear()
        self.book_cache.clear()
        self.tree.clear()

        self.cursor.execute("SELECT * FROM readers")
        for reader_id, _ in self.cursor.fetchall():
            self.reader_cache.add(reader_id)

        self.cursor.execute("SELECT isbn, available_quantity FROM books")
        for isbn, qty in self.cursor.fetchall():
            self.book_cache[isbn] = qty

        self.cursor.execute("SELECT * FROM loans")
        for row in self.cursor.fetchall():
            loan = LoanRecord(*row)
            self.tree.insert(loan.loan_id, loan)

    def reload_database_loan(self):
        self.load_all_data()

    def get_next_id(self):
        max_id = 0
        for loan in self.tree.inorder():
            if loan.loan_id > max_id:
                max_id = loan.loan_id
        return max_id + 1

    def can_borrow(self, reader_id, isbn):
        if reader_id not in self.reader_cache:
            print(f"Bạn đọc '{reader_id}' không tồn tại.")
            return False

        if isbn not in self.book_cache:
            print(f"Sách với ISBN '{isbn}' không tồn tại.")
            return False

        if self.book_cache[isbn] <= 0:
            print("Sách đã hết, không thể mượn.")
            return False

        for loan in self.tree.inorder():
            if loan.reader_id == reader_id and loan.isbn == isbn and loan.status == "Đang mượn":
                print("Bạn đọc đang mượn sách này và chưa trả.")
                return False

        return True

    def create_loan(self, reader_id, isbn, duedays):
        if not self.can_borrow(reader_id, isbn):
            return

        loan_id = self.get_next_id()
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=duedays)
        record = LoanRecord(loan_id, reader_id, isbn, borrow_date, due_date)
        self.tree.insert(loan_id, record)
        self.book_cache[isbn] -= 1

        self.cursor.execute("""
            INSERT INTO loans (loan_id, reader_id, isbn, borrow_date, due_date, status)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (loan_id, reader_id, isbn, borrow_date.strftime("%Y-%m-%d %H:%M:%S.%f"), due_date.strftime("%Y-%m-%d %H:%M:%S.%f"), "Đang mượn"))
        self.cursor.execute("UPDATE books SET available_quantity = available_quantity - 1, borrowed_quantity = borrowed_quantity + 1 WHERE isbn = ?", (isbn,))
        self.conn.commit()
        print("Tạo phiếu mượn thành công.")
        new_ch = input("Tiếp tục tạo phiếu mượn (yes/no):")
        if new_ch.strip().lower() == "no":
            call_loan_management()
    def return_book(self, loan_id):
        record = self.tree.search(loan_id)
        if not record or record.status != "Đang mượn":
            print("Không tìm thấy phiếu hoặc sách đã được trả.")
        else:
            record.status = "Đã trả"
            record.return_date = datetime.now()
            self.book_cache[record.isbn] += 1
            self.cursor.execute("""
            UPDATE loans SET return_date=?, status=? WHERE loan_id=?
        """, (record.return_date.strftime("%Y-%m-%d %H:%M:%S.%f"), "Đã trả", loan_id))
            self.cursor.execute("UPDATE books SET available_quantity = available_quantity + 1 , borrowed_quantity = borrowed_quantity -1 WHERE isbn = ?", (record.isbn,))
            self.conn.commit()
            print("Trả sách thành công.")
        new_ch = input("Tiếp tục trả sách (yes/no):")
        if new_ch.strip().lower() == "no":
            call_loan_management()
    def delete_loan(self, loan_id):
        record = self.tree.search(loan_id)
        if not record or record.status == "Đang mượn":
            print("Không thể xoá phiếu chưa trả.")
        else:
            self.tree.delete(loan_id)
            self.cursor.execute("DELETE FROM loans WHERE loan_id=?", (loan_id,))
            self.conn.commit()
            print("Xoá phiếu thành công.")
        new_ch = input("Tiếp tục xóa phiếu mượn (yes/no):")
        if new_ch.strip().lower() == "no":
            call_loan_management()
    def view_loans(self):
        for loan in self.tree.inorder():
            print(loan)
        call_loan_management()
    def filter_by_reader(self, reader_id):
        print(f"Lịch sử mượn của bạn đọc {reader_id}:")
        for loan in self.tree.inorder():
            if loan.reader_id == reader_id:
                print(loan)
        new_ch = input("Tiếp tục xem lịch sử mượn (yes/no):")
        if new_ch.strip().lower() == "no":
            call_loan_management()
    def filter_by_isbn(self, isbn):
        print(f"Lịch sử mượn của sách ISBN {isbn}:")
        for loan in self.tree.inorder():
            if loan.isbn == isbn:
                print(loan)
        new_ch = input("Tiếp tục xem lịch sử mượn (yes/no):")
        if new_ch.strip().lower() == "no":
            call_loan_management()
    def view_overdue(self):
        print("Danh sách sách quá hạn:")
        today = datetime.now()
        for loan in self.tree.inorder():
            if loan.status == "Đang mượn" and loan.due_date < today:
                print(loan)
        call_loan_management()
def loan_choice():
    manager = LoanManager(conn)
    ch = input("Nhập lựa chọn của bạn (1 - 8): ").strip()
    while True:
        if ch == "1":
            reader_id = input("Mã bạn đọc: ").strip()
            isbn = input("ISBN sách: ").strip()
            duedays = int(input("Số ngày mượn: ").strip() or 30)
            manager.create_loan(reader_id, isbn, duedays)
        elif ch == "2":
            loan_id = int(input("ID phiếu mượn: ").strip())
            manager.return_book(loan_id)

        elif ch == "3":
            loan_id = int(input("ID phiếu mượn cần xoá: ").strip())
            manager.delete_loan(loan_id)

        elif ch == "4":
            manager.view_loans()

        elif ch == "5":
            reader_id = input("Mã bạn đọc: ").strip()
            manager.filter_by_reader(reader_id)

        elif ch == "6":
            isbn = input("ISBN sách: ").strip()
            manager.filter_by_isbn(isbn)

        elif ch == "7":
            manager.view_overdue()

        elif ch == "8":
            print("Trở về menu chính.")
            from main import main
            main()
            break

        else:
            print("Lựa chọn không hợp lệ. Hãy thử lại.")
