from datetime import datetime, timedelta

class Habit:
    """
    Represents a habit with periodic check-offs and streak calculation.
    """
    def __init__(self, id: int, name: str, spec: str, periodicity: str,
                 created_at: datetime, check_offs: list[datetime] = None):
        self.id = id
        self.name = name
        self.spec = spec
        if periodicity not in ['daily', 'weekly']:
            raise ValueError("Periodicity must be 'daily' or 'weekly'")
        self.periodicity = periodicity
        self.created_at = created_at
        self.check_offs = sorted(check_offs or [])

    def add_check_off(self, timestamp: datetime = None):
        if timestamp is None:
            timestamp = datetime.now()
        self.check_offs.append(timestamp)
        self.check_offs.sort()

    def _period_start(self, dt: datetime) -> datetime.date:
        """Return the start of the period containing dt."""
        if self.periodicity == 'daily':
            return dt.date()
        # weekly: start of ISO week (Monday)
        return dt.date() - timedelta(days=dt.weekday())

    def longest_streak(self) -> int:
        """Calculate the longest consecutive streak of completed periods."""
        if not self.check_offs:
            return 0

        # Use min/max from actual check-offs for period range (more accurate for tests)
        oldest_ts = min(self.check_offs)
        newest_ts = max(self.check_offs)

        step_days = 7 if self.periodicity == 'weekly' else 1
        step = timedelta(days=step_days)

        # Start from oldest period (round down)
        start_period = self._period_start(oldest_ts)

        # End: today's period (include current day/week)
        today_period = self._period_start(datetime.now())

        # Generate ordered periods from oldest to today
        periods = []
        current = start_period
        while current <= today_period:
            periods.append(current)
            current += step

        # Completed periods (at least one check-off)
        completed = {self._period_start(ts) for ts in self.check_offs}

        # Calculate max consecutive
        streak = 0
        max_streak = 0
        for p in periods:
            if p in completed:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0

        return max_streak