#Viết các cấu trúc dữ liệu cần dùng: HashTable, AVL Tree, Merge Sort, Hàm đếm tần suấtsuất
import textwrap

def print_wrapped_table(headers, rows, col_widths, padding_char='-'):
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
# Cấu trúc dữ liệu HashTable
class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class LinkedListForHash:
    def __init__(self):
        self.head = None

    def insert(self, key, value):
        node = self.head
        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next
        new_node = HashNode(key, value)
        new_node.next = self.head
        self.head = new_node

    def search(self, key):
        node = self.head
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def delete(self, key):
        prev = None
        node = self.head
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.head = node.next
                return
            prev = node
            node = node.next

    def get_all_key_value_pairs(self):
        result = []
        node = self.head
        while node:
            result.append((node.key, node.value))
            node = node.next
        return result

class HashTable:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.size = 0
        self.table = [LinkedListForHash() for _ in range(capacity)]

    def _hash_function(self, key):
        key = str(key)  # Ensure key is a string
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.capacity
        return hash_value

    def insert(self, key, value):
        index = self._hash_function(key)
        if self.table[index].search(key) is None:
            self.size += 1
        self.table[index].insert(key, value)

    def search(self, key):
        index = self._hash_function(key)
        return self.table[index].search(key)

    def delete(self, key):
        index = self._hash_function(key)
        if self.table[index].search(key) is not None:
            self.size -= 1
        self.table[index].delete(key)

    def get_all_values(self):
        result = []
        for bucket in self.table:
            result.extend([value for _, value in bucket.get_all_key_value_pairs()])
        return result
    
# Cấu trúc AVL Tree
# avl_tree.py

class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class BSTree:
    def __init__(self):
        self.root = None

    def clear(self):
        self.root = None

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        return x

    def insert(self, key, value):
        self.root = self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node, key, value):
        if node is None:
            return TreeNode(key, value)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        else:
            # Trường hợp key trùng: cập nhật giá trị
            node.value = value
            return node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Cân bằng AVL sau khi chèn
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node.value if node else None
        return self._search_recursive(node.left, key) if key < node.key else self._search_recursive(node.right, key)

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.key, node.value = temp.key, temp.value
            node.right = self._delete_recursive(node.right, temp.key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Cân bằng lại sau khi xoá
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
              # Giới hạn đệ quy để tránh treo máyaa
            self._inorder_recursive(node.right, result)

# Cấu trúc Merge Sort
def merge_sort(arr, key_func, reverse=False):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key_func)
    right = merge_sort(arr[mid:], key_func)
    return merge(left, right, key_func,reverse)

def merge(left, right, key_func, reverse):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if (key_func(left[i]) <= key_func(right[j]) and not reverse) or \
        (key_func(left[i]) > key_func(right[j]) and reverse):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
# Hàm đếm tần suất:
def count_frequencies(list_of_objects, attribute_name_to_count):
    """
    Đếm tần suất của thuộc tính bất kỳ từ danh sách đối tượng,
    sử dụng HashTable đã định nghĩa sẵn.
    Trả về danh sách tuple (key, count)
    """
    frequency_table = HashTable()
    
    for obj in list_of_objects:
        try:
            key = getattr(obj, attribute_name_to_count)
        except AttributeError:
            print(f"Cảnh báo: Không có thuộc tính '{attribute_name_to_count}'")
            continue

        current_count = frequency_table.search(key)
        if current_count is None:
            frequency_table.insert(key, 1)
        else:
            frequency_table.insert(key, current_count + 1)
    
    # Trả kết quả dưới dạng danh sách tuple
    result = []
    for bucket in frequency_table.table:
        for key, value in bucket.get_all_key_value_pairs():
            result.append((key, value))
    
    return result
