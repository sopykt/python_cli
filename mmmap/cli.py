"""This module provides the mmmap CLI."""
# mmmap/cli.py

from pathlib import Path
from typing import List, Optional

import typer

from mmmap import ERRORS, __app_name__, __version__, config, database, mmmap

from mmmap import __app_name__, __version__

# creates an explicit Typer application, app
app = typer.Typer()


# define init() as a Typer command using the @app.command() decorator.
@app.command()
def init(
    # define a Typer Option instance and assign it as a default value to db_path. 
    # To provide a value for this option, your users need to use --db-path or -db followed by a database path. 
    # The prompt argument displays a prompt asking for a database location. 
    # It also allows you to accept the default path by pressing Enter.
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
) -> None:
    """Initialize the mmmap database."""
    # calls init_app() to create the application’s configuration file and to-do database.
    app_init_error = config.init_app(db_path)
    # check if the call to init_app() returns an error. 
    # If so, lines 38 to 41 print an error message. 
    # Line 42 exits the app with a typer.Exit exception and an exit code of 1 to signal 
    # that the application terminated with an error.
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    # calls init_database() to initialize the database with an empty to-do list.
    db_init_error = database.init_database(Path(db_path))
    # check if the call to init_database() returns an error. 
    # If so, then lines 49 to 52 display an error message, and line 53 exits the application. 
    # Otherwise, line 55 prints a success message in green text.
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)
        
# To print the messages in this code (above), you use typer.secho(). 
# This function takes a foreground argument, fg, 
# that allows you to use different colors when printing text to the screen. 
# Typer provides several built-in colors in typer.colors. There you’ll find RED, BLUE, GREEN, and more. 
# You can use those colors with secho() as you did here (above).

# To have an instance of Todoer with a valid database path
def get_todoer() -> mmmap.Todoer:
    # defines a conditional that checks if the application’s configuration file exists. 
    # To do so, it uses Path.exists().
    if config.CONFIG_FILE_PATH.exists():
        # If the configuration file exists, then gets the path to the database from it.
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    # The else clause runs if the file doesn’t exist. 
    else:
        # This clause prints an error message to the screen 
        typer.secho(
            'Config file not found. Please, run "mmmap init"',
            fg=typer.colors.RED,
        )
        # and exits the application with an exit code of 1 to signal an error.
        raise typer.Exit(1)
    # checks if the path to the database exists.
    if db_path.exists():
        # If so, then creates an instance of Todoer with the path as an argument.
        return mmmap.Todoer(db_path)
    # Otherwise, the else clause that starts typer.secho and prints an error message 
    else:
        typer.secho(
            'Database not found. Please, run "mmmap init"',
            fg=typer.colors.RED,
        )
        # and exits the application.
        raise typer.Exit(1)

# define add() as a Typer command using the @app.command() Python decorator.
@app.command()
def add(
    # defines description as an argument to add(). 
    # This argument holds a list of strings representing a to-do description. 
    # To build the argument, you use typer.Argument. 
    # When you pass an ellipsis (...) as the first argument to the constructor of Argument, 
    # you’re telling Typer that description is required. 
    # The fact that this argument is required means that 
    # the user must provide a to-do description at the command line
    description: List[str] = typer.Argument(...),
    # defines priority as a Typer option with a default value of 2. 
    # The option names are --priority and -p. 
    # As you decided earlier, priority only accepts three possible values: 1, 2, or 3. 
    # To guarantee this condition, you set min to 1 and max to 3. 
    # This way, Typer automatically validates the user’s input 
    # and only accepts numbers within the specified interval.
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    # gets a Todoer instance to use.
    todoer = get_todoer()
    # calls .add() on todoer and unpacks the result into todo and error.
    todo, error = todoer.add(description, priority)
    # define a conditional statement that prints an error message and exits the application 
    # if an error occurs while adding the new to-do to the database. 
    if error:
        typer.secho(
            f'Adding to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    # If no error happens, then the else clause displays a success message on the screen.
    else:
        typer.secho(
            f"""to-do: "{todo['Description']}" was added """
            f"""with priority: {priority}""",
            fg=typer.colors.GREEN,
        )
# Now you can go back to your terminal and give your add command a try: `python -m mmmap add Get some milk -p 1`

# define _version_callback(). This function takes a Boolean argument called value. 
# If value is True, then the function prints the application’s name and version using echo(). 
# After that, it raises a typer.Exit exception to exit the application cleanly.
def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

# define main() as a Typer callback using the @app.callback() decorator.
@app.callback()
def main(
    # defines version, which is of type Optional[bool]. 
    # This means it can be either of bool or None type. 
    # The version argument defaults to a typer.Option object, 
    # which allows you to create command-line options in Typer.
    version: Optional[bool] = typer.Option(
        # passes None as the first argument to the initializer of Option. 
        # This argument is required and supplies the option’s default value.
        None,
        # set the command-line names for the version option: -v and --version.
        "--version",
        "-v",
        # provides a help message for the version option.
        help="Show the application's version and exit.",
        # attaches a callback function, _version_callback(), to the version option, 
        # which means that running the option automatically calls the function.
        callback=_version_callback,
        # sets the is_eager argument to True. This argument tells Typer that 
        # the version command-line option has precedence over other commands in the current application.
        is_eager=True,
    )
) -> None:
    return

# Nice! With all this code in place, you can now give the init command a try. 
# Go back to your terminal and run the following: `python -m mmmap init`