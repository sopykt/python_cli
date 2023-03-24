"""This module provides the RP To-Do model-controller."""
# mmmap/mmmap.py
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from mmmap import DB_READ_ERROR, ID_ERROR
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

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return the current to-do list."""
        # first get the entire to-do list from the database by calling .read_todos() on the database handler.
        # The call to .read_todos() returns a named tuple, DBResponse, containing the to-do list and a return code.
        read = self._db_handler.read_todos()
        # However, you just need the to-do list, so .get_todo_list() returns the .todo_list field only.
        return read.todo_list

    # defines .set_done(). The method takes an argument called todo_id, which holds an integer 
    # representing the ID of the to-do you want to mark as done. The to-do ID is the number associated with 
    # a given to-do when you list your to-dos using the list command. 
    # Since you’re using a Python list to store the to-dos, you can turn this ID into a zero-based index 
    # and use it to retrieve the required to-do from the list.
    def set_done(self, todo_id: int) -> CurrentTodo:
        """Set a to-do as done."""
        # reads all the to-dos by calling .read_todos() on the database handler.
        read = self._db_handler.read_todos()
        # checks if any error occurs during the reading. 
        if read.error:
            # If so, then returns a named tuple, CurrentTodo, with an empty to-do and the error.
            return CurrentTodo({}, read.error)
        # starts a try … except statement to catch invalid to-do IDs that translate to invalid indices 
        # in the underlying to-do list. 
        try:
            todo = read.todo_list[todo_id - 1]
        # If an IndexError occurs, 
        except IndexError:
            # then returns a CurrentTodo instance with an empty to-do and the corresponding error code.
            return CurrentTodo({}, ID_ERROR)
        # assigns True to the "Done" key in the target to-do dictionary. 
        # This way, you’re setting the to-do as done.
        todo["Done"] = True
        # writes the update back to the database by calling .write_todos() on the database handler.
        write = self._db_handler.write_todos(read.todo_list)
        # returns a CurrentTodo instance with the target to-do and a return code indicating how the operation went.
        return CurrentTodo(todo, write.error)

    # defines .remove(). This method takes a to-do ID as an argument 
    # and removes the corresponding to-do from the database.
    def remove(self, todo_id: int) -> CurrentTodo:
        """Remove a to-do from the database using its id or index."""
        # reads the to-do list from the database by calling .read_todos() on the database handler.
        read = self._db_handler.read_todos()
        # checks if any error occurs during the reading process. 
        if read.error:
            # If so, then returns a named tuple, CurrentTodo, holding an empty to-do 
            # and the corresponding error code.
            return CurrentTodo({}, read.error)
        # starts a try … except statement to catch any invalid ID coming from the user’s input.
        try:
            # removes the to-do at index todo_id - 1 from the to-do list.
            todo = read.todo_list.pop(todo_id - 1)
        # If an IndexError occurs during this operation, 
        except IndexError:
            # then returns a CurrentTodo instance with an empty to-do and the corresponding error code.
            return CurrentTodo({}, ID_ERROR)
        # writes the updated to-do list back to the database.
        write = self._db_handler.write_todos(read.todo_list)
        # returns a CurrentTodo tuple holding the removed to-do 
        # and a return code indicating a successful operation.
        return CurrentTodo(todo, write.error)