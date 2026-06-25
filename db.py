import sqlite3
import json

DB_FILE = "bot.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    # ---------------- SETUP ----------------
    def setup(self):
        # GUILD SETTINGS
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS guild_settings (
            guild_id INTEGER PRIMARY KEY,
            log_channel INTEGER
        )
        """)

        # WARNINGS
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            guild_id INTEGER,
            reason TEXT
        )
        """)

        # ECONOMY
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS economy (
            user_id INTEGER,
            guild_id INTEGER,
            balance INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, guild_id)
        )
        """)

        # LEVELING
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS levels (
            user_id INTEGER,
            guild_id INTEGER,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, guild_id)
        )
        """)

        # BACKUPS
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            data TEXT
        )
        """)

        # ROBLOX VERIFICATION
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS roblox_verifications (
            guild_id INTEGER,
            user_id INTEGER,
            username TEXT,
            code TEXT,
            verified INTEGER DEFAULT 0,
            PRIMARY KEY (guild_id, user_id)
        )
        """)

        # STATS LOGGING
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            action TEXT,
            timestamp TEXT
        )
        """)

        self.conn.commit()

    # ---------------- LOG CHANNEL ----------------
    def set_log_channel(self, guild_id, channel_id):
        self.cursor.execute("""
        INSERT INTO guild_settings (guild_id, log_channel)
        VALUES (?, ?)
        ON CONFLICT(guild_id)
        DO UPDATE SET log_channel=excluded.log_channel
        """, (guild_id, channel_id))
        self.conn.commit()

    def get_log_channel(self, guild_id):
        self.cursor.execute(
            "SELECT log_channel FROM guild_settings WHERE guild_id=?",
            (guild_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    # ---------------- WARNINGS ----------------
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

    def remove_warning(self, user_id, guild_id):
        self.cursor.execute("""
        DELETE FROM warnings
        WHERE id = (
            SELECT id FROM warnings
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

    # ---------------- ECONOMY ----------------
    def get_balance(self, user_id, guild_id):
        self.cursor.execute("""
        SELECT balance FROM economy
        WHERE user_id=? AND guild_id=?
        """, (user_id, guild_id))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def add_balance(self, user_id, guild_id, amount):
        self.cursor.execute("""
        INSERT INTO economy (user_id, guild_id, balance)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, guild_id)
        DO UPDATE SET balance = balance + ?
        """, (user_id, guild_id, amount, amount))
        self.conn.commit()

    def remove_balance(self, user_id, guild_id, amount):
        self.cursor.execute("""
        INSERT INTO economy (user_id, guild_id, balance)
        VALUES (?, ?, 0)
        ON CONFLICT(user_id, guild_id)
        DO UPDATE SET balance = balance - ?
        """, (user_id, guild_id, amount))
        self.conn.commit()

    # ---------------- LEVELING ----------------
    def add_xp(self, user_id, guild_id, xp):
        self.cursor.execute("""
        INSERT INTO levels (user_id, guild_id, xp, level)
        VALUES (?, ?, ?, 0)
        ON CONFLICT(user_id, guild_id)
        DO UPDATE SET xp = xp + ?
        """, (user_id, guild_id, xp, xp))
        self.conn.commit()

    def get_xp(self, user_id, guild_id):
        self.cursor.execute("""
        SELECT xp FROM levels
        WHERE user_id=? AND guild_id=?
        """, (user_id, guild_id))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_level(self, user_id, guild_id):
        self.cursor.execute("""
        SELECT level FROM levels
        WHERE user_id=? AND guild_id=?
        """, (user_id, guild_id))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    # ---------------- BACKUPS ----------------
    def save_backup(self, guild_id, data):
        self.cursor.execute("""
        INSERT INTO backups (guild_id, data)
        VALUES (?, ?)
        """, (guild_id, data))
        self.conn.commit()

    def get_backups(self, guild_id):
        self.cursor.execute("""
        SELECT id, guild_id, data FROM backups
        WHERE guild_id=?
        """, (guild_id,))
        return self.cursor.fetchall()

    def get_backup(self, backup_id):
        self.cursor.execute("""
        SELECT data FROM backups
        WHERE id=?
        """, (backup_id,))
        return self.cursor.fetchone()

    # ---------------- ROBLOX ----------------
    def save_roblox_verification(self, guild_id, user_id, username, code):
        self.cursor.execute("""
        INSERT INTO roblox_verifications
        (guild_id, user_id, username, code, verified)
        VALUES (?, ?, ?, ?, 0)
        ON CONFLICT(guild_id, user_id)
        DO UPDATE SET username=excluded.username, code=excluded.code
        """, (guild_id, user_id, username, code))
        self.conn.commit()

    def get_roblox_verification(self, guild_id, user_id):
        self.cursor.execute("""
        SELECT username, code, verified
        FROM roblox_verifications
        WHERE guild_id=? AND user_id=?
        """, (guild_id, user_id))
        return self.cursor.fetchone()

    def set_roblox_verified(self, guild_id, user_id):
        self.cursor.execute("""
        UPDATE roblox_verifications
        SET verified=1
        WHERE guild_id=? AND user_id=?
        """, (guild_id, user_id))
        self.conn.commit()

    # ---------------- STATS LOGGING ----------------
    def log_join(self, guild_id, user_id, timestamp):
        self.cursor.execute("""
        INSERT INTO stats_logs (guild_id, user_id, action, timestamp)
        VALUES (?, ?, 'join', ?)
        """, (guild_id, user_id, timestamp))
        self.conn.commit()

    def log_leave(self, guild_id, user_id, timestamp):
        self.cursor.execute("""
        INSERT INTO stats_logs (guild_id, user_id, action, timestamp)
        VALUES (?, ?, 'leave', ?)
        """, (guild_id, user_id, timestamp))
        self.conn.commit()


db = Database()