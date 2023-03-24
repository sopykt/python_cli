"""This module provides the mmmap database functionality."""
# mmmap/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from mmmap import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

# define DEFAULT_DB_FILE_PATH to hold the default database file path. 
# The application will use this path if the user doesn’t provide a custom one.
DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.json"
)

# define get_database_path(). This function takes the path to the app’s config file as an argument, 
# reads the input file using ConfigParser.read(), 
# and returns a Path object representing the path to the to-do database on your file system. 
# The ConfigParser instance stores the data in a dictionary. 
# The "General" key represents the file section that stores the required information. 
# The "database" key retrieves the database path.
def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

# define init_database(). This function takes a database path and writes a string representing an empty list. 
# You call .write_text() on the database path, and the list initializes the JSON database with an empty to-do list. 
# If the process runs successfully, then init_database() returns SUCCESS. 
# Otherwise, it returns the appropriate error code.
def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text("[]")  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

# define DBResponse as a NamedTuple subclass. 
# The todo_list field is a list of dictionaries representing individual to-dos, 
# while the error field holds an integer return code.
class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int

# defines DatabaseHandler, which allows you to read and write data to the to-do database 
# using the json module from the standard library.
class DatabaseHandler:
    # define the class initializer, which takes a single argument 
    # representing the path to the database on your file system.
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    # defines .read_todos(). This method reads the to-do list from the database and deserializes it.
    def read_todos(self) -> DBResponse:
        # starts a try … except statement to catch any errors that occur while you’re opening the database. 
        # If an error occurs, then line 79 returns a DBResponse instance with an empty to-do list 
        # and a DB_READ_ERROR.
        try:
            # opens the database for reading using a with statement.
            with self._db_path.open("r") as db:
                # starts another try … except statement to catch any errors that occur 
                # while you’re loading and deserializing the JSON content from the to-do database.
                try:
                    # returns a DBResponse instance holding the result of calling json.load() 
                    # with the to-do database object as an argument. 
                    # This result consists of a list of dictionaries. Every dictionary represents a to-do. 
                    # The error field of DBResponse holds SUCCESS to signal that the operation was successful.
                    return DBResponse(json.load(db), SUCCESS)
                # catches any JSONDecodeError while loading the JSON content from the database, 
                # and line 75 returns with an empty list and a JSON_ERROR.
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        # catches any file IO problems while loading the JSON file, 
        # and line 79 returns a DBResponse instance with an empty to-do list and a DB_READ_ERROR.
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    # defines .write_todos(), which takes a list of to-do dictionaries and writes it to the database.
    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:
        # starts a try … except statement to catch any errors that occur 
        # while you’re opening the database. 
        # If an error occurs, then line 95 returns a DBResponse instance with the original to-do list 
        # and a DB_READ_ERROR.
        try:
            # uses a with statement to open the database for writing.
            with self._db_path.open("w") as db:
                # dumps the to-do list as a JSON payload into the database.
                json.dump(todo_list, db, indent=4)
            # returns a DBResponse instance holding the to-do list and the SUCCESS code.
            return DBResponse(todo_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(todo_list, DB_WRITE_ERROR)