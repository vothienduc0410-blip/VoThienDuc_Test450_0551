import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Nhập class giao diện Ui_MainWindow từ file playfair_ui.py
from ui.playfair_ui import Ui_MainWindow

class PlayFairCipher:
    def __init__(self) -> None:
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I")  # Chuyển "J" thành "I" trong khóa
        key = key.upper()
        
        # Để giữ đúng thứ tự các ký tự trong khóa mà không bị trùng lặp
        key_letters = []
        for letter in key:
            if letter not in key_letters and letter.isalpha():
                key_letters.append(letter)
                
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Bỏ chữ J
        remaining_letters = [letter for letter in alphabet if letter not in key_letters]
        
        matrix = key_letters + remaining_letters
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        return None

    def playfair_encrypt(self, plain_text, matrix):
        # Chuyển "J" thành "I" trong văn bản đầu vào
        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.upper().replace(" ", "")  # Loại bỏ khoảng trắng nếu có
        
        # Xử lý các cặp ký tự trùng nhau đứng cạnh nhau và chèn 'X'
        prepared_text = ""
        i = 0
        while i < len(plain_text):
            prepared_text += plain_text[i]
            if i + 1 < len(plain_text):
                if plain_text[i] == plain_text[i+1]:
                    prepared_text += "X"
                    i += 1
                    continue
                else:
                    prepared_text += plain_text[i+1]
            i += 2
            
        if len(prepared_text) % 2 != 0:
            prepared_text += "X"
            
        encrypted_text = ""
        for i in range(0, len(prepared_text), 2):
            pair = prepared_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
                
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper().replace(" ", "")
        decrypted_text = ""
        
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]
                
        # Khôi phục văn bản gốc (Xử lý bỏ bớt ký tự 'X' đã chèn)
        banro = ""
        i = 0
        while i < len(decrypted_text):
            if i + 2 < len(decrypted_text) and decrypted_text[i] == decrypted_text[i+2] and decrypted_text[i+1] == "X":
                banro += decrypted_text[i] + decrypted_text[i+2]
                i += 3
            else:
                banro += decrypted_text[i]
                i += 1
                
        if banro.endswith("X"):
            banro = banro[:-1]
            
        return banro

# 2. CLASS ĐIỀU KHIỂN GIAO DIỆN VÀ KẾT NỐI SỰ KIỆN GUI
class PlayFairApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Khởi tạo tầng xử lý logic Playfair Cipher
        self.cipher = PlayFairCipher()
        
        # Kết nối sự kiện tương tác của các nút bấm trên UI
        self.ui.btnCreateMatrix.clicked.connect(self.handle_create_matrix)
        self.ui.btnEncrypt.clicked.connect(self.handle_encrypt)
        self.ui.btnDecrypt.clicked.connect(self.handle_decrypt)

    def handle_create_matrix(self):
        """Đọc từ khóa từ ô input và hiển thị ma trận 5x5 trực quan lên UI"""
        key_input = self.ui.txtKeyMatrix.toPlainText().strip()
        
        if not key_input:
            QMessageBox.warning(self, "Lỗi dữ liệu", "Vui lòng nhập từ khóa để tạo ma trận!")
            return
            
        # Tạo ma trận bằng hàm logic của bạn
        matrix = self.cipher.create_playfair_matrix(key_input)
        
        # Định dạng chuỗi ma trận hiển thị đẹp mắt theo hàng và cột 5x5
        matrix_display = ""
        for row in matrix:
            matrix_display += "   ".join(row) + "\n"
            
        # Hiển thị lại vào ô txtKeyMatrix để người dùng quan sát trực quan
        self.ui.txtKeyMatrix.setPlainText(matrix_display.strip())

    def handle_encrypt(self):
        """Xử lý sự kiện khi ấn nút ENCRYPT"""
        plain_text = self.ui.txtPlainText.toPlainText().strip()
        encrypt_key = self.ui.txtEncryptKey.toPlainText().strip()
        
        if not plain_text or not encrypt_key:
            QMessageBox.warning(self, "Lỗi dữ liệu", "Vui lòng nhập đầy đủ Plain Text và Key mã hóa!")
            return
            
        # Bước 1: Tạo ma trận từ khóa dựa trên khóa mã hóa
        matrix = self.cipher.create_playfair_matrix(encrypt_key)
        # Bước 2: Thực hiện thuật toán mã hóa
        cipher_text = self.cipher.playfair_encrypt(plain_text, matrix)
        
        # Bước 3: Đẩy kết quả hiển thị sang ô Cipher Text bên phần Giải mã
        self.ui.txtCipherText.setPlainText(cipher_text)

    def handle_decrypt(self):
        """Xử lý sự kiện khi ấn nút DECRYPT"""
        cipher_text = self.ui.txtCipherText.toPlainText().strip()
        decrypt_key = self.ui.txtDecryptKey.toPlainText().strip()
        
        if not cipher_text or not decrypt_key:
            QMessageBox.warning(self, "Lỗi dữ liệu", "Vui lòng nhập đầy đủ Cipher Text và Key giải mã!")
            return
            
        # Bước 1: Tạo ma trận từ khóa dựa trên khóa giải mã
        matrix = self.cipher.create_playfair_matrix(decrypt_key)
        # Bước 2: Thực hiện thuật toán giải mã
        plain_text = self.cipher.playfair_decrypt(cipher_text, matrix)
        
        # Bước 3: Đẩy kết quả hiển thị ngược lại ô Plain Text bên phần Mã hóa
        self.ui.txtPlainText.setPlainText(plain_text)

# 3. KHỞI CHẠY CHƯƠNG TRÌNH
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  
    
    main_window = PlayFairApp()
    main_window.show()
    sys.exit(app.exec_())