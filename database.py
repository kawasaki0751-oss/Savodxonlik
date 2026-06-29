import sqlite3

def init_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(user_id, amount, category):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (user_id, amount, category) VALUES (?, ?, ?)', (user_id, amount, category))
    conn.commit()
    conn.close()

def get_total_expenses(user_id):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return result if result else 0

def reset_expenses(user_id):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    # Foydalanuvchi IDsi bo'yicha hamma qatorni o'chirish
    cursor.execute('DELETE FROM expenses WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

# MANA BU YANGI FUNKSIYANI ENG OXIRIGA QO'SHASAN:
def get_report_by_category(user_id):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category', (user_id,))
    results = cursor.fetchall()
    conn.close()
    return results