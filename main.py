from menu import menu, book_management, reader_management, loan_management
from database import create_connection, reload_database_book, reload_database_loan, reload_database_reader
from loan import LoanRecord, LoanManager
def main():
    conn, cursor = create_connection("library11.db")
    if not conn:
        print("Không thể kết nối đến cơ sở dữ liệu.")
    else:
        while True: 
            menu()
            ch = input("Nhập lựa chọn của bạn: ")
            if ch == "1":
                print("Quản lý sách")
                # Nạp lại dữ liệu sách từ cơ sở dữ liệu
                reload_database_book()
                # Gọi hàm quản lý sách từ book.py
                book_management()
            elif ch == "2":
                print("Quản lý bạn đọc")
                # Gọi hàm quản lý bạn đọc từ reader.py
                reload_database_reader()
                reader_management()
            elif ch == "3":
                print("Quản lý mượn trả sách")
                reload_database_loan(LoanManager)
                # Gọi hàm quản lý mượn trả sách từ loan.py
                loan_management()
            elif ch == "4":
                print("Thoát chương trình")
                break
            else:
                print("Lựa chọn không hợp lệ, vui lòng thử lại.")
    # Đóng kết nối khi thoát
    conn.close()
if __name__ == "__main__":
    main()

