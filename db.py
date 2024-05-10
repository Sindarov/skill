import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    def user_exists(self, user_id):
        try:
            with self.connection:
                result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()

                return bool(len(result))
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return False

    def add_user(self, user_id, referrer_id=None):
        with self.connection:
            if referrer_id != None:
                return self.cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id', 'referrer_id') VALUES (?, ?)", (user_id, referrer_id,))
            else:
                return self.cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (user_id,))

    def count_referrer(self, user_id):
        with self.connection:
            count_query = "SELECT COUNT(id) FROM users WHERE referrer_id = ?"
            count = self.cursor.execute(count_query, (user_id,)).fetchone()[0]
            update_query = "UPDATE users SET balance = ? WHERE user_id = ?"
            self.cursor.execute(update_query, (count, user_id))
            self.connection.commit()


    def get_user_balance(self, user_id):
        try:
            # Assuming you have a database connection established
            with self.connection:
                result = self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
                return result[0] if result is not None else 0
        except Exception as e:
            # Handle any exceptions (e.g., database errors)
            print(f"Error fetching user balance: {e}")
            return 0

    def deduct_balance(self, user_id, amount):
        try:
            query = "UPDATE users SET balance = balance - ? WHERE user_id = ?"
            self.cursor.execute(query, (amount, user_id))
            self.connection.commit()  # Commit the changes
            return True  # Successfully deducted the amount
        except Exception as e:
            # Handle any exceptions (e.g., database errors)
            print(f"Error deducting balance: {e}")
            return False  # Failed to deduct the amount

    def del_ref(self, user_id):
        try:
            query = "UPDATE users SET referrer_id = 0 WHERE ROWID IN (SELECT ROWID FROM users WHERE referrer_id = ? LIMIT 5);"
            self.cursor.execute(query, (user_id,))
            self.connection.commit()
        except Exception as e:
            # Handle any exceptions (e.g., database errors)
            print(f"Error deducting balance: {e}")

    def DSAT_purchased(self, user_id):
        try:
            query = "UPDATE users SET DSAT_purchased = 1 WHERE user_id = ?"

            self.cursor.execute(query, (user_id,))
            self.connection.commit()
        except Exception as e:
            # Handle any exceptions (e.g., database errors)
            print(f"Error deducting balance: {e}")

    def purchased(self, user_id):
        try:
            query = "SELECT DSAT_purchased FROM users WHERE user_id = ?"
            result = self.cursor.execute(query, (user_id,)).fetchone()
            return result[0] if result is not None else 0
        except:
            print('error')

    def purchased2(self, user_id):
        try:
            query = "SELECT DSAT_purchased2 FROM users WHERE user_id = ?"
            result = self.cursor.execute(query, (user_id,)).fetchone()
            return result[0] if result is not None else 0
        except:
            print('error')

    def DSAT_purchased2(self, user_id):
        try:
            query = "UPDATE users SET DSAT_purchased2 = 1 WHERE user_id = ?"

            self.cursor.execute(query, (user_id,))
            self.connection.commit()
        except Exception as e:
            # Handle any exceptions (e.g., database errors)
            print(f"Error deducting balance: {e}")
