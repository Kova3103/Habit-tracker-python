from functools import reduce
from habit import Habit

def get_all_habits(db) -> list[Habit]:
    """Functional: Returns all tracked habits from DB."""
    return db.get_all_habits()

def get_habits_by_periodicity(db, periodicity: str) -> list[Habit]:
    """Functional: Returns habits with given periodicity using filter."""
    return list(filter(lambda h: h.periodicity == periodicity, get_all_habits(db)))

def longest_streak_all(db) -> int:
    """Functional: Returns longest streak across all habits using reduce."""
    habits = get_all_habits(db)
    if not habits:
        return 0
    return reduce(lambda max_streak, h: max(max_streak, h.get_streak()), habits, 0)

def longest_streak_habit(db, habit_name: str) -> int:
    """Functional: Returns longest streak for a given habit using filter."""
    habits = get_all_habits(db)
    matching = list(filter(lambda h: h.name == habit_name, habits))
    return matching[0].get_streak() if matching else 0