from datetime import datetime, timedelta

class Habit:
    """
    Represents a habit with task specification and periodicity.
    
    Attributes:
        id (int): Unique identifier (from DB).
        name (str): Habit name, e.g., "Drink Water".
        periodicity (str): 'daily' or 'weekly'.
        created_at (datetime): Creation timestamp.
        check_offs (list[datetime]): List of completion timestamps.
    """
    def __init__(self, name: str, periodicity: str, created_at: datetime = None, check_offs: list = None, id: int = None):
        """
        Initializes a Habit instance.
        
        Args:
            name: Habit name.
            periodicity: 'daily' or 'weekly'.
            created_at: Optional creation time (defaults to now).
            check_offs: Optional list of check-off times.
            id: Optional DB ID.
        
        Raises:
            ValueError: If periodicity is invalid.
        """
        if periodicity not in ['daily', 'weekly']:
            raise ValueError("Periodicity must be 'daily' or 'weekly'")
        self.id = id
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now()
        self.check_offs = check_offs or []

    def check_off(self, timestamp: datetime = None):
        """Checks off the habit at the given timestamp (defaults to now)."""
        if timestamp is None:
            timestamp = datetime.now()
        self.check_offs.append(timestamp)

    def get_streak(self):
        """
        Calculates the longest streak of consecutive periods with at least one check-off.
        
        Returns:
            int: Longest streak count.
        """
        if not self.check_offs:
            return 0
        sorted_check_offs = sorted(self.check_offs)
        if self.periodicity == 'daily':
            period_delta = timedelta(days=1)
            def get_period_start(dt: datetime) -> datetime:
                return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        else:  # weekly, start on Monday
            period_delta = timedelta(days=7)
            def get_period_start(dt: datetime) -> datetime:
                monday = dt - timedelta(days=dt.weekday())  # 0 = Monday
                return monday.replace(hour=0, minute=0, second=0, microsecond=0)

        # Get unique period starts
        period_starts = {get_period_start(dt) for dt in sorted_check_offs}
        period_starts = sorted(period_starts)

        current_streak = 1
        max_streak = 1
        for i in range(1, len(period_starts)):
            if period_starts[i] == period_starts[i - 1] + period_delta:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        return max_streak

    def __repr__(self):
        return f"Habit({self.name}, {self.periodicity}, streak={self.get_streak()})"