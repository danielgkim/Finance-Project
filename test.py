



import sqlite3
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class PersonalFinanceTracker:
    def __init__(self, db_name='finance.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL
        )
        ''')
        
        # Create categories table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL
        )
        ''')
        
        # Insert default categories
        default_categories = [
            ('Salary', 'income'),
            ('Food', 'expense'),
            ('Transport', 'expense'),
            ('Utilities', 'expense'),
            ('Entertainment', 'expense'),
            ('Shopping', 'expense'),
            ('Healthcare', 'expense')
        ]
        
        cursor.executemany('''
        INSERT OR IGNORE INTO categories (name, type)
        VALUES (?, ?)
        ''', default_categories)
        
        self.conn.commit()
    
    def add_transaction(self, date, category, description, amount, trans_type):
    # Adding transaction data
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO transactions (date, category, description, amount, type)
        VALUES (?, ?, ?, ?, ?)
        ''', (date, category, description, amount, trans_type))
        self.conn.commit()

        # Fetch all transaction data for regression (example fetching amounts and dates)
        cursor.execute('SELECT amount FROM transactions ORDER BY date')
        amounts = [row[0] for row in cursor.fetchall()]
        dates = range(len(amounts))  # Using index as a proxy for dates for simplicity
    
        # Perform linear regression
        X = np.array(dates).reshape(-1, 1)  # Dates as features
        y = np.array(amounts)  # Amounts as targets
        model = LinearRegression().fit(X, y)
    
        # Save regression coefficients if needed
       # intercept = model.intercept_
        #slope = model.coef_[0]
       # cursor.execute('''
        #INSERT INTO regression_results (slope, intercept)
        #VALUES (?, ?)
        #''', (slope, intercept))
        #self.conn.commit()
    
    def add_category(self, name, category_type):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO categories (name, type)
        VALUES (?, ?)
        ''', (name, category_type))
        self.conn.commit()
    
    def get_balance(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT 
            SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) 
        FROM transactions
        ''')
        return cursor.fetchone()[0] or 0
    
    def get_monthly_summary(self, year, month):
        cursor = self.conn.cursor()
        date_pattern = f'{year}-{month:02d}-%'
        
        # Get income
        cursor.execute('''
        SELECT category, SUM(amount) 
        FROM transactions 
        WHERE type = 'income' AND date LIKE ?
        GROUP BY category''', (date_pattern,))
        income = dict(cursor.fetchall())
        
        # Get expenses
        cursor.execute('''
        SELECT category, SUM(amount) 
        FROM transactions 
        WHERE type = 'expense' AND date LIKE ?
        GROUP BY category
        ''', (date_pattern,))
        expenses = dict(cursor.fetchall())
        
        return {
            'income': income,
            'expenses': expenses,
            'total_income': sum(income.values()) if income else 0,
            'total_expenses': sum(expenses.values()) if expenses else 0,
            'net_savings': (sum(income.values()) if income else 0) - 
                         (sum(expenses.values()) if expenses else 0)
        }
    
    def get_transactions(self, start_date=None, end_date=None, category=None):
        query = 'SELECT * FROM transactions WHERE 1=1'
        params = []
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        if category:
            query += ' AND category = ?'
            params.append(category)
            
        query += ' ORDER BY date DESC'
        
        return pd.read_sql_query(query, self.conn, params=params)
    
    def close(self):
        self.conn.close()

# Example usage
def main():
    tracker = PersonalFinanceTracker()
    
    # Add some sample transactions
    tracker.add_transaction('2024-10-01', 'Salary', 'Monthly salary', 5000, 'income')
    tracker.add_transaction('2024-10-01', 'Streams', 'Distrokid', 5000, 'income')
    tracker.add_transaction('2024-10-02', 'Music', 'Music Video', 150, 'expense')
    tracker.add_transaction('2024-10-03', 'Transport', 'Promo', 30, 'expense')
    
    # Get current balance
    print(f"Current balance: ${tracker.get_balance():.2f}")
    
    # Get monthly summary
    summary = tracker.get_monthly_summary(2024, 10)
    print("\nMonthly Summary:")
    print(f"Total Income: ${summary['total_income']:.2f}")
    print(f"Total Expenses: ${summary['total_expenses']:.2f}")
    print(f"Net Savings: ${summary['net_savings']:.2f}")
    
    # Get all transactions
    print("\nRecent Transactions:")
    transactions = tracker.get_transactions()
    print(transactions)
    
    tracker.close()

if __name__ == "__main__":
    main()