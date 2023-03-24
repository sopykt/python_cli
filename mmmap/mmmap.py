"""This module provides the RP To-Do model-controller."""
# mmmap/mmmap.py
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from mmmap import DB_READ_ERROR
from mmmap.database import DatabaseHandler

# create a subclass of typing.NamedTuple called CurrentTodo with two fields todo and error
# Subclassing NamedTuple allows you to create named tuples with type hints for their named fields. 
# For example, the todo field above holds a dictionary with keys of type str and values of type Any. 
# The error field holds an int value.
class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int

# This class uses composition, so it has a DatabaseHandler component 
# to facilitate direct communication with the to-do database.
class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
    
    # defines .add(), which takes description and priority as arguments. The description is a list of strings. 
    # Typer builds this list from the words you enter at the command line to describe the current to-do. 
    # In the case of priority, it’s an integer value representing the to-do’s priority. 
    # The default is 2, indicating a medium priority.
    def add(self, description: List[str], priority: int = 2) -> CurrentTodo:
        """Add a new to-do to the database."""
        # concatenates the description components into a single string using .join().
        description_text = " ".join(description)
        # add a period (".") to the end of the description if the user doesn’t add it.
        if not description_text.endswith("."):
            description_text += "."
        # build a new to-do from the user’s input.
        todo = {
            "Description": description_text,
            "Priority": priority,
            "Done": False,
        }
        # reads the to-do list from the database by calling .read_todos() on the database handler.
        read = self._db_handler.read_todos()
        # checks if .read_todos() returned a DB_READ_ERROR. 
        if read.error == DB_READ_ERROR:
            # If so, then returns a named tuple, CurrentTodo, containing the current to-do and the error code.
            return CurrentTodo(todo, read.error)
        # appends the new to-do to the list.
        read.todo_list.append(todo)
        # writes the updated to-do list back to the database by calling .write_todos() on the database handler.
        write = self._db_handler.write_todos(read.todo_list)
        # returns an instance of CurrentTodo with the current to-do and an appropriate return code.
        return CurrentTodo(todo, write.error)