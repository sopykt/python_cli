"""This module provides the mmmap config functionality."""
# mmmap/config.py

# imports configparser. This module provides the ConfigParser class, 
# which allows you to handle config files with a structure similar to INI files.
import configparser
# imports Path from pathlib. This class provides a cross-platform way to handle system paths.
from pathlib import Path
# imports typer.
import typer
#  import a bunch of required objects from mmmap.
from mmmap import (
    DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__
)

# creates CONFIG_DIR_PATH to hold the path to the app’s directory. 
# To get this path, you call get_app_dir() with the application’s name as an argument. 
# This function returns a string representing the path to a directory where you can store configurations.
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
# defines CONFIG_FILE_PATH to hold the path to the configuration file itself.
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

# defines init_app(). This function initializes the application’s configuration file and database.
def init_app(db_path: str) -> int:
    """Initialize the application."""
    # calls the _init_config_file() helper function, which you define in lines 47 to 56. 
    # Calling this function creates the configuration directory using Path.mkdir(). 
    # It also creates the configuration file using Path.touch(). 
    # Finally, _init_config_file() returns the proper error codes if something wrong happens 
    # during the creation of the directory and file. It returns SUCCESS if everything goes okay.
    config_code = _init_config_file()
    # checks if an error occurs during the creation of the directory and configuration file, 
    # and line 35 returns the error code accordingly.
    if config_code != SUCCESS:
        return config_code
    # calls the _create_database() helper function, which creates the database. 
    # This function returns the appropriate error codes if something happens while creating the database. 
    # It returns SUCCESS if the process succeeds.
    database_code = _create_database(db_path)
    # checks if an error occurs during the creation of the database. 
    # If so, then line 23 returns the corresponding error code.
    if database_code != SUCCESS:
        return database_code
    # returns SUCCESS if everything runs okay.
    return SUCCESS

def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS

def _create_database(db_path: str) -> int:
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return DB_WRITE_ERROR
    return SUCCESS

# With this code, you’ve finished setting up the application’s configuration file 
# to store the path to the database. 
# You’ve also added code to create the database as a JSON file. 
# Now you can write code for initializing the database and getting it ready for use. 