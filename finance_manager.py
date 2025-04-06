import sqlite3
from datetime import datetime, timedelta
import bcrypt
import pandas as pd

class FinanceManager:
    def __init__(self, user_id=None):
        self.conn = sqlite3.connect('finance.db', check_same_thread=False)
        self.user_id = user_id
        self.create_tables()
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        # Initialize sample data only if the users table is empty
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            self._create_sample_user()
            self._create_sample_accounts()
            self._create_sample_categories()
            self._create_sample_transactions()
            self.conn.commit()

    def _create_sample_user(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       ('mohamed', bcrypt.hashpw('123'.encode('utf-8'), bcrypt.gensalt())))

    def _create_sample_accounts(self):
        accounts = [
            ('البنك الأهلي', 5000.0, 1000.0),
            ('محفظة النقود', 2000.0, 500.0),
            ('بطاقة الائتمان', -1000.0, -2000.0)
        ]
        cursor = self.conn.cursor()
        for name, balance, min_balance in accounts:
            cursor.execute("INSERT INTO accounts (user_id, name, balance, min_balance, created_at) VALUES (?, ?, ?, ?, ?)",
                           (1, name, balance, min_balance, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def _create_sample_categories(self):
        categories = [
            (1, 'IN', 'مرتب'),
            (1, 'IN', 'مكافأة'),
            (1, 'OUT', 'طعام'),
            (1, 'OUT', 'مواصلات'),
            (1, 'OUT', 'تسوق')
        ]
        cursor = self.conn.cursor()
        for acc_id, trans_type, name in categories:
            cursor.execute("INSERT INTO categories (account_id, transaction_type, name) VALUES (?, ?, ?)",
                           (acc_id, trans_type, name))

    def _create_sample_transactions(self):
        transactions = [
            (1, 100.0, 'IN', 'مرتب شهر يناير', 'تحويل بنكي', 'مرتب', '2023-01-01', 1),
            (1, 50.0, 'OUT', 'سوبر ماركت', 'بطاقة ائتمان', 'طعام', '2023-01-05', 1),
            (2, 20.0, 'OUT', 'تاكسي', 'كاش', 'مواصلات', '2023-01-10', 1),
            (3, 200.0, 'OUT', 'ملابس', 'بطاقة ائتمان', 'تسوق', '2023-01-15', 1),
            (1, 500.0, 'IN', 'مكافأة أداء', 'تحويل بنكي', 'مكافأة', '2023-01-20', 1)
        ]
        cursor = self.conn.cursor()
        for acc_id, amount, trans_type, desc, method, category, date, user_id in transactions:
            cursor.execute("""
                INSERT INTO transactions 
                (account_id, amount, type, description, payment_method, category, date, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (acc_id, amount, trans_type, desc, method, category, date, user_id))

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            ''')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
            
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    name TEXT,
                    balance REAL,
                    min_balance REAL,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(username)
                )
            ''')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id)')
            
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    date TEXT,
                    type TEXT,
                    amount REAL,
                    account_id INTEGER,
                    description TEXT,
                    payment_method TEXT,
                    category TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(username),
                    FOREIGN KEY (account_id) REFERENCES accounts(id)
                )
            ''')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id)')

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER,
                    transaction_type TEXT,
                    name TEXT,
                    FOREIGN KEY (account_id) REFERENCES accounts(id)
                )
            ''')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_categories_account_id ON categories(account_id)')

    def add_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with self.conn:
            try:
                self.conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
                self.conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def verify_user(self, username, password):
        with self.conn:
            cursor = self.conn.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return result and bcrypt.checkpw(password.encode('utf-8'), result[0])

    # ... other methods
