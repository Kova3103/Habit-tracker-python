# Habit Tracker App

**Course**: Object Oriented and Functional Programming with Python (DLBDSOOFPP01)  
**Institution**: IU International University of Applied Sciences  
**Portfolio Assignment**: Final submission – Task 1: Create a Habit Tracking App  
**Author**: Denis Kovačević  
**GitHub**: [https://github.com/Kova3103/Habit-tracker-python](https://github.com/Kova3103/Habit-tracker-python)  
**Last Updated**: February 2026

## Project Overview

This is a backend habit tracking application developed in Python as the final portfolio project for the course. The app allows users to:

- Define and manage habits with daily or weekly periodicity.
- Check off (complete) habits to build streaks.
- Persist data across sessions using SQLite.
- Analyze habits using functional programming (pure functions with `filter`, `map`, `reduce`).
- View longest streaks (historical max) and current ongoing streaks.

Key features:
- OOP design: `Habit` class for encapsulation, `HabitTracker` for persistence and management.
- Functional analytics module (`analytics.py`): pure, side-effect-free functions.
- CLI built with Click: clean commands for create, check-off, delete, list, analyze.
- 5 predefined habits with 4 weeks of simulated example data (test fixture).
- Unit tests covering creation, check-offs, streaks, analytics, and predefined data.

The project meets all acceptance criteria from the assignment:
- Python 3.7+ with modern code.
- Custom implementation (no third-party habit tools).
- Docstrings and comments.
- Persistence with SQLite (preferred over JSON).
- CLI API.
- Analytics using FP paradigm (minimal required functions + extras).
- Unit test suite.

## Requirements

- **Python**: 3.7 or later (tested on 3.10+)
- **Dependencies** (two external):
  - `click` (for CLI)
  - `pytest` (for unit tests)
- **Built-in libraries**: `sqlite3`, `datetime`, `functools`, `random`, `unittest`
- **Operating System**: Windows (primary), macOS/Linux compatible

No additional installations needed beyond Click and Pytest.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Kova3103/Habit-tracker-python.git
   cd Habit-tracker-python

2. **Create and activate a virtual environment**:
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

3. **Install dependencies**:
    pip install -r requirements.txt

4. **Run the application**:
    python main.py --help
    (First run creates habits.db and loads 5 predefined habits with 4 weeks of example data.)

5. **Run unit tests**:
    python tests.py
    (Verifies habit creation, check-offs, streaks, analytics, and predefined data.)


## Usage – All Commands
Run python main.py --help for quick overview.

1. create – Create a new habit
    Syntax:
    - python main.py create --name "<name>" --spec "<description>" --periodicity <daily|weekly>
    Example:
    - python main.py create --name "Yoga" --spec "Practice 20 min" --periodicity daily
    Output:
    - Created: Yoga (ID: 6) - daily

2. check-off – Complete a habit
    Syntax:
    - python main.py check-off --id <ID>
    Example:
    - python main.py check-off --id 1
    Output:
    - Checked off habit ID 1
    Note: Multiple check-offs in the same period are allowed (only ≥1 counts for streak).

3. delete – Delete a habit
    Syntax:
    - python main.py delete --id <ID>
    Example:
    - python main.py delete --id 6
    Output:
    - Deleted habit ID 6

4. list – List all habits
    Syntax:
    - python main.py list
    Output (example):
    - Your habits:
    ID 1 | Drink Water          | daily     | Drink 2L per day               | Last check: 2026-01-30 11:52
    ID 2 | Read Book            | daily     | Read 20 pages                  | Last check: 2026-01-30 10:13
    ...

5. analyze-all – Analyze habits
    Syntax:
    - python main.py analyze-all
    Interactive:
    - Analyze which habits? (all, daily, weekly) [all]:
    Output (example – daily group):
    - Daily habits Analysis:
    Drink Water (daily): Longest 3 | Current 1 periods | Last check: 2026-01-31 14:25
    Read Book (daily): Longest 28 | Current 28 periods | Last check: 2026-01-30 10:13

    Overall longest streak in this group: 28 periods
    Achieved by: Read Book

6. longest-for – Longest streak for one habit
    Syntax:
    - python main.py longest-for --id <ID>
    Example:
    - python main.py longest-for --id 1
    Output:
    - 'Drink Water' (daily): Longest 3 | Current 1 periods | Last check: 2026-01-31 14:25
    
Predefined Habits & Simulated Data
On first run (or empty DB), 5 habits are loaded automatically:

Daily:
- Drink Water
- Read Book
- Exercise

Weekly:
- Grocery Shopping
- Clean House


Each has 4 weeks (28 days) of simulated check-offs:

Daily: Last check-off = yesterday
Weekly: Last check-off = last week
Realistic misses to test streak resets
Random time variation (±2 hours around midday)

