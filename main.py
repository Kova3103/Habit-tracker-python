import click
from tracker import HabitTracker
from analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    longest_streak_all,
    longest_streak_for_habit
)

tracker = HabitTracker()  # loads DB + predefined habits if empty

@click.group()
def cli():
    """Habit Tracker CLI – Track and analyze daily/weekly habits."""
    pass

@cli.command()
@click.option('--name', required=True, help='Habit name')
@click.option('--spec', required=True, help='Description')
@click.option('--periodicity', required=True, type=click.Choice(['daily', 'weekly']))
def create(name, spec, periodicity):
    """Create a new habit."""
    habit = tracker.create_habit(name, spec, periodicity)
    click.echo(f"Created: {habit.name} (ID: {habit.id}) - {periodicity}")

@cli.command(name='check-off')
@click.option('--id', required=True, type=int, help='Habit ID')
def check_off(id):
    """Check off a habit (mark as done today)."""
    tracker.check_off_habit(id)
    click.echo(f"Checked off habit ID {id}")

@cli.command(name='delete')
@click.option('--id', required=True, type=int, help='Habit ID')
def delete(id):
    """Delete a habit and its history."""
    tracker.delete_habit(id)
    click.echo(f"Deleted habit ID {id}")

@cli.command(name='list')
def list_all():
    """List all habits with their current longest streak."""
    habits = get_all_habits(tracker.get_all_habits())
    if not habits:
        click.echo("No habits yet. Use 'create' to add one.")
        return

    click.echo("Your habits (ID | Name | Periodicity | Description | Longest Streak):")
    for h in habits:
        streak = longest_streak_for_habit(h)
        click.echo(f"  {h.id:2} | {h.name:20} | {h.periodicity:8} | {h.spec:30} | {streak} periods")

@cli.command(name='analyze-all')
def analyze_all():
    """Analyze all habits: show longest streak for each + overall max."""
    habits = get_all_habits(tracker.get_all_habits())
    if not habits:
        click.echo("No habits to analyze.")
        return

    click.echo("Habit Analysis:")
    max_streak = 0
    max_habit = None
    for h in habits:
        streak = longest_streak_for_habit(h)
        click.echo(f"  {h.name} ({h.periodicity}): {streak} periods")
        if streak > max_streak:
            max_streak = streak
            max_habit = h.name

    click.echo(f"\nOverall longest streak: {max_streak} periods (habit: {max_habit})")

@cli.command(name='longest-for')
@click.option('--id', required=True, type=int, help='Habit ID')
def longest_for(id):
    """Show longest streak for one specific habit."""
    habits = get_all_habits(tracker.get_all_habits())
    habit = next((h for h in habits if h.id == id), None)
    if not habit:
        click.echo(f"Habit ID {id} not found.")
        return
    streak = longest_streak_for_habit(habit)
    click.echo(f"Longest streak for '{habit.name}' ({habit.periodicity}): {streak} periods")

if __name__ == '__main__':
    cli()