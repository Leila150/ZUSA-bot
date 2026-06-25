import sqlite3

DB_FILE = "bot.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS guild_settings (
            guild_id INTEGER PRIMARY KEY,
            log_channel INTEGER
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            guild_id INTEGER,
            reason TEXT
        )
        """)

        self.conn.commit()

    # ---------- LOG CHANNEL ----------
    def set_log_channel(self, guild_id, channel_id):
        self.cursor.execute("""
        INSERT INTO guild_settings (guild_id, log_channel)
        VALUES (?, ?)
        ON CONFLICT(guild_id)
        DO UPDATE SET log_channel=?
        """, (guild_id, channel_id, channel_id))
        self.conn.commit()

    def get_log_channel(self, guild_id):
        self.cursor.execute(
            "SELECT log_channel FROM guild_settings WHERE guild_id=?",
            (guild_id,)
        )

        result = self.cursor.fetchone()
        return result[0] if result else None

    # ---------- WARNINGS ----------
    def add_warning(self, user_id, guild_id, reason):
        self.cursor.execute("""
        INSERT INTO warnings (
            user_id,
            guild_id,
            reason
        )
        VALUES (?, ?, ?)
        """, (user_id, guild_id, reason))

        self.conn.commit()

    def get_warnings(self, user_id, guild_id):
        self.cursor.execute("""
        SELECT reason
        FROM warnings
        WHERE user_id=? AND guild_id=?
        """, (user_id, guild_id))

        return self.cursor.fetchall()

    def remove_warning(self, user_id, guild_id):
        self.cursor.execute("""
        DELETE FROM warnings
        WHERE id = (
            SELECT id
            FROM warnings
            WHERE user_id=? AND guild_id=?
            LIMIT 1
        )
        """, (user_id, guild_id))

        self.conn.commit()

    def clear_warnings(self, user_id, guild_id):
        self.cursor.execute("""
        DELETE FROM warnings
        WHERE user_id=? AND guild_id=?
        """, (user_id, guild_id))

        self.conn.commit()


db = Database()
