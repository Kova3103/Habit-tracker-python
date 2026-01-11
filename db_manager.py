import sqlite3
from datetime import datetime
from habit import Habit

class DBManager:
    """
    Manages SQLite database for habits and check-offs.
    """
    def __init__(self, db_name: str = 'habits.db'):
        """Initializes connection and creates tables if not exist."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Creates database tables."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS check_offs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
            )
        ''')
        self.conn.commit()

    def create_habit(self, name: str, periodicity: str):
        """Creates a new habit and returns the Habit object."""
        created_at = datetime.now().isoformat()
        self.cursor.execute('INSERT INTO habits (name, periodicity, created_at) VALUES (?, ?, ?)',
                           (name, periodicity, created_at))
        self.conn.commit()
        habit_id = self.cursor.lastrowid
        return Habit(name, periodicity, datetime.fromisoformat(created_at), [], habit_id)

    def get_all_habits(self):
        """Retrieves all habits with their check-offs."""
        self.cursor.execute('SELECT * FROM habits')
        habits = []
        for row in self.cursor.fetchall():
            habit_id, name, periodicity, created_at = row
            self.cursor.execute('SELECT timestamp FROM check_offs WHERE habit_id = ?', (habit_id,))
            check_offs = [datetime.fromisoformat(ts[0]) for ts in self.cursor.fetchall()]
            habits.append(Habit(name, periodicity, datetime.fromisoformat(created_at), check_offs, habit_id))
        return habits

    def add_check_off(self, habit_id: int, timestamp: datetime = None):
        """Adds a check-off for a habit at the given timestamp (defaults to now)."""
        if timestamp is None:
            timestamp = datetime.now()
        ts_iso = timestamp.isoformat()
        self.cursor.execute('INSERT INTO check_offs (habit_id, timestamp) VALUES (?, ?)', (habit_id, ts_iso))
        self.conn.commit()

    def delete_habit(self, habit_id: int):
        """Deletes a habit and its check-offs."""
        self.cursor.execute('DELETE FROM check_offs WHERE habit_id = ?', (habit_id,))
        self.cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        self.conn.commit()

    def close(self):
        """Closes the database connection."""
        self.conn.close()