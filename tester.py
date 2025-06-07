import textwrap

def print_wrapped_table(headers, rows, col_widths, padding_char='-'):
    """
    In một bảng với tiêu đề và nhiều dòng dữ liệu, trong đó mỗi ô sẽ tự động xuống dòng
    nếu nội dung dài hơn chiều rộng cột quy định.
    
    Args:
        headers (List[str]): Danh sách tiêu đề cột.
        rows (List[List[str]]): Dữ liệu bảng, mỗi phần tử là một dòng (list các ô).
        col_widths (List[int]): Chiều rộng cố định của từng cột.
        padding_char (str): Ký tự dùng để phân cách dòng, mặc định là '-'.
    """
    def wrap_row(row):
        wrapped_cells = [
            textwrap.wrap(str(cell), width=col_widths[i]) for i, cell in enumerate(row)
        ]
        max_lines = max(len(cell) for cell in wrapped_cells)
        lines = []
        for i in range(max_lines):
            line = []
            for j, cell_lines in enumerate(wrapped_cells):
                content = cell_lines[i] if i < len(cell_lines) else ''
                line.append(f"{content:<{col_widths[j]}}")
            lines.append(" | ".join(line))
        return lines

    # In tiêu đề
    header_line = " | ".join([f"{header:<{col_widths[i]}}" for i, header in enumerate(headers)])
    print(header_line)
    print(padding_char * len(header_line))

    # In từng dòng dữ liệu
    for row in rows:
        wrapped_lines = wrap_row(row)
        for line in wrapped_lines:
            print(line)
        print(padding_char * len(header_line))  # ngăn cách giữa các dòng
headers = [
    "ISBN", "Tiêu đề", "Thể loại", "Tác giả",
    "SL nhập thêm", "SL tổng", "SL còn", "SL đã mượn"
]
col_widths = [9, 25, 10, 10, 15, 15, 15, 10]

rows = [
    [
        "123456789",
        "aaaaaaaaaaaaaaaaaaabbbbbbbbbbaaaaaaaaaaaaaaaaaaabbbbbbbbbb",
        "Trinh thám",
        "Tác giả A",
        "10",
        "50",
        "40",
        "10"
    ],
    [
        "987654321",
        "Một tiêu đề khác cực kỳ dài mà vẫn cần in trong khung cột Tiêu đề",
        "Giả tưởng",
        "Tác giả B",
        "5",
        "20",
        "15",
        "5"
    ]
]

print_wrapped_table(headers, rows, col_widths)
