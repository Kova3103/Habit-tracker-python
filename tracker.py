import sqlite3
from datetime import datetime, timedelta
from habit import Habit

class HabitTracker:
    """
    Manages habits, persistence in SQLite, and predefined data.
    """
    def __init__(self, db_path='habits.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
        if not self.get_all_habits():
            self._load_predefined()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                spec TEXT,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS check_offs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        ''')
        self.conn.commit()

    def create_habit(self, name: str, spec: str, periodicity: str) -> Habit:
        if periodicity not in ['daily', 'weekly']:
            raise ValueError("Periodicity must be 'daily' or 'weekly'")
        created_at = datetime.now()
        self.cursor.execute('''
            INSERT INTO habits (name, spec, periodicity, created_at)
            VALUES (?, ?, ?, ?)
        ''', (name, spec, periodicity, created_at.isoformat()))
        self.conn.commit()
        habit_id = self.cursor.lastrowid
        return Habit(habit_id, name, spec, periodicity, created_at)

    def get_all_habits(self) -> list[Habit]:
        self.cursor.execute('SELECT * FROM habits')
        habits = []
        for row in self.cursor.fetchall():
            hid, name, spec, per, cat = row
            created_at = datetime.fromisoformat(cat)
            self.cursor.execute('SELECT timestamp FROM check_offs WHERE habit_id = ? ORDER BY timestamp', (hid,))
            check_offs = [datetime.fromisoformat(ts[0]) for ts in self.cursor.fetchall()]
            habits.append(Habit(hid, name, spec, per, created_at, check_offs))
        return habits

    def check_off_habit(self, habit_id: int, timestamp: datetime = None):
        if timestamp is None:
            timestamp = datetime.now()
        self.cursor.execute('INSERT INTO check_offs (habit_id, timestamp) VALUES (?, ?)',
                            (habit_id, timestamp.isoformat()))
        self.conn.commit()

    def delete_habit(self, habit_id: int):
        self.cursor.execute('DELETE FROM check_offs WHERE habit_id = ?', (habit_id,))
        self.cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        self.conn.commit()

    def _load_predefined(self):
        predefined = [
            ("Brush Teeth", "Brush twice a day", "daily"),
            ("Exercise", "Workout 30 min", "daily"),
            ("Read Book", "Read 20 pages", "daily"),
            ("Clean House", "Deep clean", "weekly"),
            ("Grocery Shopping", "Buy weekly supplies", "weekly")
        ]
        for name, spec, per in predefined:
            habit = self.create_habit(name, spec, per)
            now = datetime.now()
            for i in range(28):
                if i % 5 != 0:  # realistic misses
                    dt = now - timedelta(days=i, hours=12)
                    self.check_off_habit(habit.id, dt)

    def close(self):
        """Close the database connection."""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            self.conn = None