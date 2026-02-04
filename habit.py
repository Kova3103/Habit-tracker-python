from datetime import datetime, timedelta

class Habit:
    """
    Represents a habit with periodic check-offs and streak calculations.
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
        """Start of the period containing dt (Monday for weekly, day for daily)."""
        if self.periodicity == 'daily':
            return dt.date()
        return dt.date() - timedelta(days=dt.weekday())

    def longest_streak(self) -> int:
        """Longest historical streak (all-time max)."""
        if not self.check_offs:
            return 0

        oldest = min(self.check_offs)
        newest = max(self.check_offs)

        step_days = 7 if self.periodicity == 'weekly' else 1
        step = timedelta(days=step_days)

        start = self._period_start(oldest)
        end = self._period_start(newest)

        periods = []
        current = start
        while current <= end:
            periods.append(current)
            current += step

        completed = {self._period_start(ts) for ts in self.check_offs}

        streak = 0
        max_streak = 0
        for p in periods:
            if p in completed:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0

        return max_streak

    def current_streak(self) -> int:
        """
        Current ongoing streak up to the most recent completed period.
        - Last check-off yesterday/last week → current = longest (chain active).
        - Check off today → current += 1 (extends chain).
        - Miss current period → current = 0 next period.
        """
        if not self.check_offs:
            return 0

        step_days = 7 if self.periodicity == 'weekly' else 1
        step = timedelta(days=step_days)

        last_ts = max(self.check_offs)
        last_period = self._period_start(last_ts)
        today_period = self._period_start(datetime.now())

        completed = {self._period_start(ts) for ts in self.check_offs}

        # If last check-off is before today → chain active up to last period
        if last_period < today_period:
            # Count from last_period back
            streak = 1
            current = last_period - step
            while current in completed:
                streak += 1
                current -= step
            return streak

        # Last check-off is today → count from today back
        streak = 0
        current = today_period
        while current in completed:
            streak += 1
            current -= step

        return streak