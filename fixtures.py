from datetime import datetime, timedelta
from db_manager import DBManager
from habit import Habit  # For type hinting, optional

def load_fixtures(db_file: str = 'habits.db'):
    """
    Loads 5 predefined habits (3 daily, 2 weekly) with 4 weeks of example tracking data.
    Run this script once to populate the DB for testing/demos.
    """
    db = DBManager(db_file)
    
    # Predefined habits with days to check off (0-27 for past 4 weeks, simulate misses for realism)
    habits_data = [
        ("Drink Water", "daily", [0, 1, 2, 4, 5, 6, 8, 9, 11, 12, 13, 15, 16, 17, 19, 20, 22, 23, 24, 26, 27]),  # Some misses
        ("Read Book", "daily", list(range(28))),  # Perfect streak
        ("Meditate", "daily", [0, 3, 6, 9, 12, 15, 18, 21, 24, 27]),  # Every 3 days
        ("Gym", "weekly", [0, 7, 14, 21]),  # Every week
        ("Clean House", "weekly", [0, 7, 21])   # Miss one week
    ]
    
    start_date = datetime.now() - timedelta(days=28)  # Start 4 weeks ago
    
    for name, periodicity, check_days in habits_data:
        habit = db.create_habit(name, periodicity)
        for day in check_days:
            ts = start_date + timedelta(days=day)
            db.add_check_off(habit.id, ts)
    
    db.close()
    print("Fixtures loaded successfully.")

if __name__ == "__main__":
    load_fixtures()