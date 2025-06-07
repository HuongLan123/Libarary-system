print("Chương trình quản lý thư viện")
from book import book_choice
from reader import reader_choice
from loan import loan_choice
#Tạo menu
def menu():
    print("Hệ thống quản lý thư viện")
    print("1. Quản lý sách")
    print("2. Quản lý bạn đọc")
    print("3. Quản lý mượn trả sách")
    print("4. Thoát")
#Các menu con 
# Chức năng quản lý sách
def book_management():
    print("Chọn chức năng quản lý sách")
    print("1. Thêm sách")
    print("2. Xóa sách")
    print("3. Tìm kiếm sách")
    print("4. Cập nhật thông tin sách")
    print("5. Sắp xếp sách")
    print("6. Xem danh sách các sách hiện tại")
    print("7. Trở về menu chính")
    book_choice()
# Chức năng quản lý bạn đọc
def reader_management():
    print("Chọn chức năng quản lý bạn đọc")
    print("\nChọn chức năng quản lý bạn đọc:")
    print("1. Thêm bạn đọc")
    print("2. Xóa bạn đọc")
    print("3. Tìm kiếm bạn đọc")
    print("4. Cập nhật bạn đọc")
    print("5. Sắp xếp bạn đọc")
    print("6. Xem danh sách")
    print("7. Trở về menu chính")    
    reader_choice()
# Chức năng quản lý mượn trả sách
def loan_management():
    print("Chọn chức năng quản lý mượn trả sách")
    print("1. Mượn sách")
    print("2. Trả sách")
    print("3. Xóa phiếu mượn")
    print("4. Lịch sử mượn trả")
    print("5. Thông tin mượn trả theo bạn đọc")
    print("6. Thông tin mượn trả theo sách")
    print("7. Thống kê sách quá hạn")
    print("8. Trở về menu chính")
    loan_choice()

