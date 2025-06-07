def test_book(isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity):
    """
    Kiểm tra dữ liệu hợp lệ của một quyển sách trước khi thêm vào hệ thống.
    
    Trả về: (True, "") nếu hợp lệ
            (False, lý do lỗi) nếu không hợp lệ
    """
    # Kiểm tra trường rỗng
    if not isbn.strip():
        return False, "ISBN không được để trống."
    if not title.strip():
        return False, "Tiêu đề sách không được để trống."
    if not genre.strip():
        return False, "Thể loại sách không được để trống."
    if not author.strip():
        return False, "Tác giả sách không được để trống."

    # Kiểm tra kiểu dữ liệu và giá trị số hợp lệ
    try:
        added_quantity = int(added_quantity)
        quantity = int(quantity)
        available_quantity = int(available_quantity)
        borrowed_quantity = int(borrowed_quantity)
    except ValueError:
        return False, "Các trường số lượng phải là số nguyên."

    # Kiểm tra giá trị âm
    if any(q < 0 for q in [added_quantity, quantity, available_quantity, borrowed_quantity]):
        return False, "Số lượng không được là số âm."

    # Kiểm tra mâu thuẫn logic
    if available_quantity > quantity:
        return False, "Số lượng có sẵn không thể lớn hơn tổng số lượng sách."
    if borrowed_quantity > quantity:
        return False, "Số lượng đã mượn không thể lớn hơn tổng số lượng sách."
    if available_quantity + borrowed_quantity != quantity:
        return False, "Tổng số lượng phải bằng đã mượn + có sẵn."

    return True, ""
