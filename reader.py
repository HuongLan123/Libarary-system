# Viết các chức năng: add_reader, delete_reader, search_reader, update_reader, sort_readers
# reader.py
from cautrucdulieu import HashTable, merge_sort, print_wrapped_table
import sqlite3
import csv
def call_reader_management():
    from menu import reader_management
    reader_management()
# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect("library11.db")
cursor = conn.cursor()

# Định nghĩa lớp Reader
class Reader:
    def __init__(self, reader_id, name):
        self.reader_id = reader_id
        self.name = name

    def __str__(self):
        return f"{self.reader_id} | {self.name}"

    def __eq__(self, other):
        return isinstance(other, Reader) and self.reader_id == other.reader_id

    def __hash__(self):
        return hash(self.reader_id)

reader_table = HashTable()
headers = ["MSSV", "Tên bạn đọc"]
col_widths = [15, 30]

def reader_choice():
    ch = input("Nhập lựa chọn của bạn (1-7): ")
    while True:
        if ch not in map(str, range(1, 8)):
            print("Lựa chọn không hợp lệ.")
            continue
        if ch == "1":
            add_reader()
        elif ch == "2":
            delete_reader()
        elif ch == "3":
            search_reader()
        elif ch == "4":
            update_reader()
        elif ch == "5":
            sort_readers()
        elif ch == "6":
            display_readers()
        elif ch == "7":
            from main import main
            main()
            break
def add_reader_file():
    filename = input("Nhập tên file (VD: readerreader.csv): ").strip()
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            readerss = csv.DictReader(csvfile)
            for row in readerss:
                reader_id = row["MSSV"]
                name = row["Name"]
                reader = Reader(reader_id, name)
                if not reader_table.search(reader_id):
                    reader_table.insert(reader_id, reader)
                    print(f"Thêm bạn đọc '{reader_id}' thành công.")
                    cursor.execute("""
        INSERT INTO readers (reader_id, namename)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (reader_id, name))
                    conn.commit()
                else:
                    print(f"Bạn đọc có MSSV'{reader_id}' đã tồn tại.")
    except FileNotFoundError:
        print(f"Không tìm thấy file '{filename}'")
        return 
    except Exception as e:
        print(f"Lỗi khi thêm sách từ file: {e}")
        return
def add_reader_terminal():
    reader_id = input("Nhập MSSV: ").strip()
    name = input("Nhập tên bạn đọc: ").strip()
    if not reader_id or not name:
        print("Mã số sinh viên và tên không được để trống.")
        return
    if reader_table.search(reader_id):
        print("Bạn đọc đã tồn tại.")
        return
    reader = Reader(reader_id, name)
    reader_table.insert(reader_id, reader)
    cursor.execute("INSERT INTO readers (MSSV, name) VALUES (?, ?)", (reader_id, name))
    conn.commit()
    print("Thêm bạn đọc thành công.")
def add_reader():
    print("Chọn phương thức thêm người đọc:")
    print("1. Thêm người đọc từ file")
    print("2. Thêm người đọc từ bàn phím")
    print("3. Trở về menu chính")
    while True:
        choice = input("Nhập lựa chọn của bạn (1 - 3): ")
        if choice == "1":
            add_reader_file()
        elif choice == "2":
            add_reader_terminal()        
        elif choice == "3":
            call_reader_management()
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")
def delete_reader():
    reader_id = input("Nhập MSSV cần xóa: ").strip()
    if reader_table.search(reader_id):
        reader_table.delete(reader_id)
        cursor.execute("DELETE FROM readers WHERE MSSV = ?", (reader_id,))
        conn.commit()
        print("Xóa bạn đọc thành công.")
    else:
        print("Không tìm thấy bạn đọc.")
    call_reader_management()
def search_reader():
    keyword = input("Nhập từ khóa tìm kiếm theo MSSV hoặc tên: ").strip().lower()
    result = []
    for reader in reader_table.get_all_values():
        if keyword in reader.reader_id.lower() or keyword in reader.name.lower():
            result.append([reader.reader_id, reader.name])
    if result:
        print_wrapped_table(headers, result, col_widths)
    else:
        print("Không tìm thấy bạn đọc nào.")
    call_reader_management()
def update_reader():
    reader_id = input("Nhập MSSV cần cập nhật: ").strip()
    reader = reader_table.search(reader_id)
    if not reader:
        print("Không tìm thấy bạn đọc.")
        return
    print(f"Thông tin hiện tại: MSSV = {reader.reader_id}, Tên = {reader.name}")
    new_name = input("Nhập tên mới (Enter để giữ nguyên): ").strip()
    if new_name:
        reader.name = new_name
        cursor.execute("UPDATE readers SET name = ? WHERE MSSV = ?", (new_name, reader_id))
        conn.commit()
        print("Cập nhật thành công.")
    else:
        print("Không có thay đổi.")
    reader_table.insert(reader.reader_id, reader)
    call_reader_management()
def sort_readers():
    readers = reader_table.get_all_values()
    reverse = input("Sắp xếp giảm dần? (True/False): ").strip().lower() == "true"
    sorted_readers = merge_sort(readers, key_func=lambda r: r.reader_id, reverse=reverse)
    data = [[r.reader_id, r.name] for r in sorted_readers]
    print_wrapped_table(headers, data, col_widths)
    call_reader_management()
def display_readers():
    all_readers = reader_table.get_all_values()
    data = [[r.reader_id, r.name] for r in all_readers]
    print_wrapped_table(headers, data, col_widths)
    call_reader_management()

