# Manages habit creation, check-offs, and persistence using SQLite database operations.
import sqlite3
from datetime import datetime, timedelta
import random
from habit import Habit

class HabitTracker:
    """Manages habits and their check-offs in a SQLite database."""

    def __init__(self, db_path='habits.db'):
        """Initialize database connection and create tables."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
        # Load predefined habits if the database is empty
        if not self.get_all_habits():
            self._load_predefined()

    def _create_tables(self):
        """Create habits and check_offs tables if they don't exist."""
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
        """Create and store a new habit in the database."""
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
        """Return all habits with their check-off history."""
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
        """Record a completion for a habit."""
        if timestamp is None:
            timestamp = datetime.now()
        self.cursor.execute('INSERT INTO check_offs (habit_id, timestamp) VALUES (?, ?)',
                            (habit_id, timestamp.isoformat()))
        self.conn.commit()

    def delete_habit(self, habit_id: int):
        """Delete a habit and all its check-offs."""
        self.cursor.execute('DELETE FROM check_offs WHERE habit_id = ?', (habit_id,))
        self.cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        self.conn.commit()

    

    def close(self):
        """Close the database connection if it exists."""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            self.conn = None
    
    def _load_predefined(self):
        """Load 5 predefined habits with 4 weeks of sample data."""
        habits_data = [
            ("Drink Water", "Drink 2L per day", "daily", [1,2,3,5,6,7,9,10,12,13,14,16,17,18,20,21,23,24,25,27,28]),
            ("Read Book", "Read 20 pages", "daily", list(range(1,29))),  # perfect 28-day streak
            ("Exercise", "60 min workout", "daily", [1,4,7,10,13,16,19,22,25,28]),
            ("Grocery Shopping", "Buy weekly groceries", "weekly", [7,14,21,28]),  # last week
            ("Clean House", "Deep clean", "weekly", [7,14,28])   # missed one week
        ]

        start_date = datetime.now() - timedelta(days=28)

        for name, spec, periodicity, check_days in habits_data:
            habit = self.create_habit(name, spec, periodicity)
            for day in check_days:
                base_ts = start_date + timedelta(days=day)
                midday = base_ts.replace(hour=12, minute=0, second=0, microsecond=0)
                random_offset = timedelta(seconds=random.randint(-7200, 7200))
                ts = midday + random_offset
                self.check_off_habit(habit.id, ts)

        print("Predefined habits loaded (last check-off yesterday/last week).")
