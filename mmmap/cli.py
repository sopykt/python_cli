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

# define list_all() as a Typer command using the @app.command() decorator. 
# The name argument to this decorator sets a custom name for the command, which is list here. 
# Note that list_all() doesn’t take any argument or option. It just lists the to-dos 
# when the user runs list from the command line.
@app.command(name="list")
def list_all() -> None:
    """List all to-dos."""
    # gets the Todoer instance that you’ll use.
    todoer = get_todoer()
    # gets the to-do list from the database by calling .get_todo_list() on todoer.
    todo_list = todoer.get_todo_list()
    # define a conditional statement to check if there’s at least one to-do in the list. 
    # If not, then the if code block prints an error message to the screen and exits the application.
    if len(todo_list) == 0:
        typer.secho(
            "There are no tasks in the to-do list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    # prints a top-level header to present the to-do list. In this case, secho() takes an additional 
    # Boolean argument called bold, which enables you to display text in a bolded font format.
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    # define and print the required columns to display the to-do list in a tabular format.
    columns = (
        "ID.  ",
        "| Priority  ",
        "| Done  ",
        "| Description  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    # run a for loop to print every single to-do on its own row with appropriate padding and separators.
    for id, todo in enumerate(todo_list, 1):
        desc, priority, done = todo.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE,
        )
    # prints a line of dashes with a final line feed character (\n) to visually separate the to-do list 
    # from the next command-line prompt.
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)
    # Then run the application with the command `python -m mmmap list`

# define set_done() as a Typer command with the usual @app.command() decorator. 
# In this case, you use complete for the command name. 
@app.command(name="complete")
# The set_done() function takes an argument called todo_id, 
# which defaults to an instance of typer.Argument. 
# This instance will work as a required command-line argument.
def set_done(todo_id: int = typer.Argument(...)) -> None:
    """Complete a to-do by setting it as done using its TODO_ID."""
    # gets the usual Todoer instance.
    todoer = get_todoer()
    # sets the to-do with the specific todo_id as done by calling .set_done() on todoer.
    todo, error = todoer.set_done(todo_id)
    # checks if any error occurs during the process. 
    if error:
        # If so, then print an appropriate error message 
        typer.secho(
            f'Completing to-do # "{todo_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        # and exit the application with an exit code of 1.
        raise typer.Exit(1)
    # If no error occurs, 
    else:
        # then print a success message in green font.
        typer.secho(
            f"""to-do # {todo_id} "{todo['Description']}" completed!""",
            fg=typer.colors.GREEN,
        )

# define remove() as a Typer CLI command.
@app.command()
def remove(
    # defines todo_id as an argument of type int. 
    # In this case, todo_id is a required instance of typer.Argument.
    todo_id: int = typer.Argument(...),
    # defines force as an option for the remove command. 
    # It’s a Boolean option that allows you to delete a to-do without confirmation.
    force: bool = typer.Option(
        # This option defaults to False
        False,
        # and its flags are --force and -f.
        "--force",
        "-f",
        # defines a help message for the force option.
        help="Force deletion without confirmation.",
    ),
) -> None:
    """Remove a to-do using its TODO_ID."""
    # creates the required Todoer instance.
    todoer = get_todoer()

    # define an inner function called _remove(). 
    # It’s a helper function that allows you to reuse the remove functionality.
    def _remove():
        # The function removes a to-do using its ID. To do that, it calls .remove() on todoer.
        todo, error = todoer.remove(todo_id)
        if error:
            typer.secho(
                f'Removing to-do # {todo_id} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"""to-do # {todo_id}: '{todo["Description"]}' was removed""",
                fg=typer.colors.GREEN,
            )

    # checks the value of force. A True value means that the user wants to remove the to-do 
    # without confirmation.
    if force:
        # In this situation, calls _remove() to run the remove operation.
        _remove()
    # starts an else clause that runs if force is False.
    else:
        # gets the entire to-do list from the database.
        todo_list = todoer.get_todo_list()
        # define a try … except statement that retrieves the desired to-do from the list.
        try:
            todo = todo_list[todo_id - 1]
        # If an IndexError occurs,
        except IndexError:
            # then prints an error message,
            typer.secho("Invalid TODO_ID", fg=typer.colors.RED)
            # and exits the application.
            raise typer.Exit(1)
        # call Typer’s confirm() and store the result in delete. 
        # This function provides an alternative way to ask for confirmation. 
        delete = typer.confirm(
            # It allows you to use a dynamically created confirmation prompt like the following line.
            f"Delete to-do # {todo_id}: {todo['Description']}?"
        )
        # checks if delete is True,
        if delete:
            # in which case calls _remove().
            _remove()
        else:
            # Otherwise, communicates that the operation was canceled.
            typer.echo("Operation canceled")

# define remove_all() as a Typer command using the @app.command() decorator 
# with clear as the command name.
@app.command(name="clear")
def remove_all(
    # define force as a Typer Option. It’s a required option of the Boolean type.
    # The prompt argument asks the user to enter a proper value to force,
    # which can be either y or n.
    force: bool = typer.Option(
        ...,
        prompt="Delete all to-dos?",
        # provides a help message for the force option.
        help="Force deletion without confirmation.",
    ),
) -> None:
    """Remove all to-dos."""
    # gets the usual Todoer instance.
    todoer = get_todoer()
    # checks if force is True. 
    if force:
        # If so, then the if code block removes all the to-dos from the database using .remove_all().
        error = todoer.remove_all().error
        # If something goes wrong during this process,
        if error:
            # the application prints an error message
            typer.secho(
                f'Removing to-dos failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            # and exits.
            raise typer.Exit(1)
        # Otherwise,
        else:
            # it prints a success message.
            typer.secho("All to-dos were removed", fg=typer.colors.GREEN)
    else:
        # runs if the user cancels the remove operation by supplying a false value,
        # indicating no, to force.
        typer.echo("Operation canceled")

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