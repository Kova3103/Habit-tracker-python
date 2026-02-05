import click
from datetime import datetime
from tracker import HabitTracker
from analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    longest_streak_for_habit
)

# Initialize tracker with error handling
try:
    tracker = HabitTracker()  # Try to initialize
except Exception as e:
    click.echo(f"Startup error: {e}")
    click.echo("Try deleting 'habits.db' and rerun.")
    exit(1)

@click.group()
def cli():
    """Habit Tracker CLI – Track and analyze daily/weekly habits."""
    pass

@cli.command()
@click.option('--name', required=True, help='Habit name')
@click.option('--spec', required=True, help='Description')
@click.option('--periodicity', required=True, type=click.Choice(['daily', 'weekly']))
def create(name, spec, periodicity):
    """Create a new habit with name, description, and periodicity."""
    habit = tracker.create_habit(name, spec, periodicity)
    click.echo(f"Created: {habit.name} (ID: {habit.id}) - {periodicity}")

@cli.command(name='check-off')
@click.option('--id', required=True, type=int, help='Habit ID')
def check_off(id):
    """Record a completion for the specified habit."""
    tracker.check_off_habit(id)
    click.echo(f"Checked off habit ID {id}")

@cli.command(name='delete')
@click.option('--id', required=True, type=int, help='Habit ID')
def delete(id):
    """Remove a habit and all its check-offs from the tracker."""
    tracker.delete_habit(id)
    click.echo(f"Deleted habit ID {id}")

@cli.command(name='list')
def list_all():
    """List all habits."""
    habits = get_all_habits(tracker.get_all_habits())
    if not habits:
        click.echo("No habits yet.")
        return
    click.echo("Your habits:")
    for h in habits:
        last_check = max(h.check_offs) if h.check_offs else "Never"
        if isinstance(last_check, datetime):
            last_check = last_check.strftime("%Y-%m-%d %H:%M")
        click.echo(f"  ID {h.id:2} | {h.name:20} | {h.periodicity:8} | {h.spec:30} | Last check: {last_check}")

@cli.command(name='analyze-all')
def analyze_all():
    """Analyze habit streaks by group (all, daily, or weekly)."""
    choice = click.prompt(
        "Analyze which habits?",
        type=click.Choice(['all', 'daily', 'weekly'], case_sensitive=False),
        default='all'
    )

    if choice == 'all':
        habits = get_all_habits(tracker.get_all_habits())
        group_name = "All habits"
    else:
        habits = get_habits_by_periodicity(tracker.get_all_habits(), choice)
        group_name = f"{choice.capitalize()} habits"

    if not habits:
        click.echo(f"No {choice} habits found.")
        return

    click.echo(f"\n{group_name} Analysis:")
    max_longest = 0
    top_habits_longest = []

    # Calculate and display metrics for each habit
    for h in habits:
        longest = longest_streak_for_habit(h)
        current = h.current_streak() if hasattr(h, 'current_streak') else 0
        last_check = max(h.check_offs) if h.check_offs else "Never"
        if isinstance(last_check, datetime):
            last_check = last_check.strftime("%Y-%m-%d %H:%M")

        click.echo(f"  {h.name:20} ({h.periodicity}): Longest {longest} | Current {current} periods  | Last check: {last_check}")

        # Track habits with longest streak
        if longest > max_longest:
            max_longest = longest
            top_habits_longest = [h.name]
        elif longest == max_longest:
            top_habits_longest.append(h.name)

    top_habits_str = ", ".join(top_habits_longest)
    click.echo(f"\nOverall longest streak in this group: {max_longest} periods")
    click.echo(f"Achieved by: {top_habits_str}")

@cli.command(name='longest-for')
@click.option('--id', required=True, type=int, help='Habit ID')
def longest_for(id):
    """Display longest and current streak for a specific habit."""
    habits = get_all_habits(tracker.get_all_habits())
    habit = next((h for h in habits if h.id == id), None)
    if not habit:
        click.echo(f"Habit ID {id} not found.")
        return
    longest = longest_streak_for_habit(habit)
    current = habit.current_streak() if hasattr(habit, 'current_streak') else 0
    last_check = max(habit.check_offs) if habit.check_offs else "Never"
    if isinstance(last_check, datetime):
        last_check = last_check.strftime("%Y-%m-%d %H:%M")
    click.echo(f"'{habit.name}' ({habit.periodicity}): Longest {longest} | Current {current} periods | Last check: {last_check}")

if __name__ == '__main__':
    cli()