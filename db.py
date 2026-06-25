import sqlite3

DB_FILE = "bot.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        # WARNINGS
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            guild_id INTEGER,
            reason TEXT
        )
        """)

        self.conn.commit()

    # ---------- WARNINGS ----------
    def add_warning(self, user_id, guild_id, reason):
        self.cursor.execute("""
        INSERT INTO warnings (user_id, guild_id, reason)
        VALUES (?, ?, ?)
        """, (user_id, guild_id, reason))
        self.conn.commit()

    def get_warnings(self, user_id, guild_id):
        self.cursor.execute("""
        SELECT reason FROM warnings
        WHERE user_id=? AND guild_id=?
        """, (user_id, guild_id))
        return self.cursor.fetchall()

    def clear_warnings(self, user_id, guild_id):
        self.cursor.execute("""
        DELETE FROM warnings
        WHERE user_id=? AND guild_id=?
        """, (user_id, guild_id))
        self.conn.commit()


db = Database()