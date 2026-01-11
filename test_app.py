import pytest
from datetime import datetime, timedelta
from habit import Habit
from db_manager import DBManager
from analytics import longest_streak_all, longest_streak_habit, get_habits_by_periodicity

def test_habit_streak_daily():
    h = Habit("Test Daily", "daily")
    start = datetime.now() - timedelta(days=5)
    h.check_off(start)
    h.check_off(start + timedelta(days=1))
    h.check_off(start + timedelta(days=2))
    h.check_off(start + timedelta(days=4))  # Miss day 3
    assert h.get_streak() == 3

def test_habit_streak_weekly():
    h = Habit("Test Weekly", "weekly")
    start = datetime.now() - timedelta(days=21)  # 3 weeks ago
    h.check_off(start)
    h.check_off(start + timedelta(days=7))
    h.check_off(start + timedelta(days=21))  # Miss week 2
    assert h.get_streak() == 2

def test_db_crud():
    db = DBManager(':memory:')  # In-memory for test
    h = db.create_habit("Test", "daily")
    db.add_check_off(h.id, datetime.now() - timedelta(days=1))
    db.add_check_off(h.id, datetime.now())
    habits = db.get_all_habits()
    assert len(habits) == 1
    assert habits[0].get_streak() == 2
    db.delete_habit(h.id)
    assert len(db.get_all_habits()) == 0
    db.close()

def test_analytics():
    db = DBManager(':memory:')
    h1 = db.create_habit("Daily1", "daily")
    db.add_check_off(h1.id, datetime.now() - timedelta(days=1))
    db.add_check_off(h1.id, datetime.now())
    h2 = db.create_habit("Weekly1", "weekly")
    db.add_check_off(h2.id, datetime.now())
    assert longest_streak_all(db) == 2
    assert longest_streak_habit(db, "Daily1") == 2
    assert len(get_habits_by_periodicity(db, "daily")) == 1
    db.close()