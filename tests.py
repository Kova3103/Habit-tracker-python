import unittest
import os
from datetime import datetime, timedelta
from habit import Habit
from tracker import HabitTracker
from analytics import get_all_habits, get_habits_by_periodicity, longest_streak_all, longest_streak_for_habit


class TestHabitTracker(unittest.TestCase):
    """Unit tests for the Habit Tracker application."""

    TEST_DB = 'test.db'

    @classmethod
    def setUpClass(cls):
        """Set up a fresh test database before all tests."""
        if os.path.exists(cls.TEST_DB):
            os.remove(cls.TEST_DB)
        cls.tracker = HabitTracker(db_path=cls.TEST_DB)

    @classmethod
    def tearDownClass(cls):
        """Clean up test database after all tests complete."""
        if hasattr(cls, 'tracker') and hasattr(cls.tracker, 'close'):
            cls.tracker.close()
        if os.path.exists(cls.TEST_DB):
            try:
                os.remove(cls.TEST_DB)
            except PermissionError:
                print("Warning: test.db locked - manual cleanup needed")

    def setUp(self):
        """Reset tracker state before each test."""
        for habit in self.tracker.get_all_habits():
            self.tracker.delete_habit(habit.id)

    def test_create_habit(self):
        """Verify habit creation stores correct metadata."""
        habit = self.tracker.create_habit("Test Habit", "Test description", "daily")
        self.assertIsNotNone(habit)
        self.assertEqual(habit.name, "Test Habit")

    def test_check_off_habit(self):
        """Verify check-off recording persists to database."""
        habit = self.tracker.create_habit("Drink Water", "Drink 2L", "daily")
        self.tracker.check_off_habit(habit.id)
        loaded = self.tracker.get_all_habits()[0]
        self.assertEqual(len(loaded.check_offs), 1)

    def test_longest_streak_no_breaks(self):
        """Test longest streak calculation with consecutive completions."""
        habit = Habit(1, "Perfect", "Test", "daily", datetime.now() - timedelta(days=10))
        for i in range(7):
            habit.add_check_off(datetime.now() - timedelta(days=i))
        self.assertEqual(habit.longest_streak(), 7)

    def test_longest_streak_with_breaks(self):
        """Test longest streak calculation with gaps in completions."""
        habit = Habit(1, "Breaks", "Test", "daily", datetime.now() - timedelta(days=15))
        for i in [0,1,2,3,7,8,9]:
            habit.add_check_off(datetime.now() - timedelta(days=i))
        self.assertEqual(habit.longest_streak(), 4)

    def test_predefined_habits_loaded(self):
        """Verify predefined habits load with correct periodicity distribution."""
        self.tracker._load_predefined()
        habits = self.tracker.get_all_habits()
        self.assertEqual(len(habits), 5)
        self.assertEqual(len([h for h in habits if h.periodicity == "daily"]), 3)

    def test_analytics_functions(self):
        """Test analytics functions with multiple habits and check-offs."""
        h1 = self.tracker.create_habit("Ex", "Run", "daily")
        h2 = self.tracker.create_habit("Read", "Pages", "daily")

        # Persist check-offs to database via tracker
        now = datetime.now()
        for i in range(5):
            self.tracker.check_off_habit(h1.id, now - timedelta(days=i))
        for i in range(8):
            self.tracker.check_off_habit(h2.id, now - timedelta(days=i))

        habits = self.tracker.get_all_habits()
        self.assertEqual(longest_streak_all(habits), 8)

if __name__ == '__main__':
    unittest.main(verbosity=2)