import sqlite3
import os

class DBManager:
    def __init__(self, db_name='database/data.db'):
        # Tạo thư mục nếu chưa có
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def setup_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                skills TEXT
            )
        ''')
        self.conn.commit()

    def insert_mock_data(self):
        self.cursor.execute('DELETE FROM Jobs') # Xóa dữ liệu cũ nếu chạy lại
        # Dữ liệu tập trung vào mảng vi mạch, bán dẫn và nhúng
        mock_jobs = [
            ("IC Design Engineer", "Intel", "Verilog, SystemVerilog, Python, C++"),
            ("Digital Design Verification", "Marvell", "SystemVerilog, UVM, Python, C++"),
            ("Embedded Software Engineer", "Bosch", "C, C++, Python, RTOS"),
            ("Hardware Engineer", "Viettel", "Verilog, FPGA, C++"),
            ("Physical Design Engineer", "FPT Semi", "Python, TCL, EDA")
        ]
        self.cursor.executemany('INSERT INTO Jobs (title, company, skills) VALUES (?, ?, ?)', mock_jobs)
        self.conn.commit()
        print("Đã tạo Database và nạp dữ liệu mẫu thành công.")

    def get_all_skills_from_db(self):
        self.cursor.execute('SELECT skills FROM Jobs')
        return [row[0] for row in self.cursor.fetchall()]