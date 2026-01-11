import click
from db_manager import DBManager
from analytics import get_all_habits, get_habits_by_periodicity, longest_streak_all, longest_streak_habit

@click.group()
def cli():
    """Habit Tracker CLI - Manage and analyze habits."""
    pass

@cli.command()
@click.option('--name', prompt='Habit name')
@click.option('--periodicity', prompt='Periodicity (daily/weekly)')
def create(name, periodicity):
    """Create a new habit."""
    db = DBManager()
    habit = db.create_habit(name, periodicity)
    click.echo(f"Created habit: {habit}")
    db.close()

@cli.command()
@click.option('--habit_id', prompt='Habit ID (from list)', type=int)
def checkoff(habit_id):
    """Check off a habit for the current period."""
    db = DBManager()
    db.add_check_off(habit_id)
    click.echo(f"Checked off habit ID {habit_id}.")
    db.close()

@cli.command()
@click.option('--habit_id', prompt='Habit ID', type=int)
def delete(habit_id):
    """Delete a habit."""
    db = DBManager()
    db.delete_habit(habit_id)
    click.echo(f"Deleted habit ID {habit_id}.")
    db.close()

@cli.command()
def list():
    """List all habits."""
    db = DBManager()
    habits = get_all_habits(db)
    for h in habits:
        click.echo(h)
    db.close()

@cli.command()
def analyze():
    """Analyze habits (streaks, lists)."""
    db = DBManager()
    click.echo("All habits:")
    click.echo(get_all_habits(db))
    periodicity = click.prompt("Periodicity to filter (daily/weekly or skip)", default="")
    if periodicity:
        click.echo(f"{periodicity.capitalize()} habits: {get_habits_by_periodicity(db, periodicity)}")
    click.echo(f"Longest streak across all habits: {longest_streak_all(db)}")
    habit_name = click.prompt("Habit name for specific streak (or skip)", default="")
    if habit_name:
        click.echo(f"Longest streak for '{habit_name}': {longest_streak_habit(db, habit_name)}")
    db.close()

if __name__ == '__main__':
    cli()