from typing import List
from habit import Habit
from functools import reduce

def get_all_habits(habits: List[Habit]) -> List[Habit]:
    """Return all currently tracked habits."""
    return habits

def get_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """Return habits matching the given periodicity."""
    return list(filter(lambda h: h.periodicity == periodicity, habits))

def longest_streak_all(habits: List[Habit]) -> int:
    """Longest streak across all habits."""
    if not habits:
        return 0
    return reduce(max, map(lambda h: h.longest_streak(), habits), 0)

def longest_streak_for_habit(habit: Habit) -> int:
    """Longest streak for a single specific habit."""
    return habit.longest_streak()
    