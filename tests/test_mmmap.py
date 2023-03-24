# tests/test_mmmap.py
import json
import pytest
# imports CliRunner from typer.testing.
from typer.testing import CliRunner

# imports a few required objects from your mmmap package.
from mmmap import DB_READ_ERROR, SUCCESS, __app_name__, __version__, cli, mmmap

# creates a CLI runner by instantiating CliRunner.
runner = CliRunner()

# defines your first unit test for testing the application’s version.
def test_version():
    # calls .invoke() on runner to run the application with the --version option. 
    # You store the result of this call in result.
    result = runner.invoke(cli.app, ["--version"])
    # asserts that the application’s exit code (result.exit_code) is equal to 0 
    # to check that the application ran successfully.
    assert result.exit_code == 0
    # asserts that the application’s version is present in the standard output, 
    # which is available through result.stdout.
    assert f"{__app_name__} v{__version__}\n" in result.stdout

    
# Typer’s CliRunner is a subclass of Click’s CliRunner. 
# Therefore, its .invoke() method returns a Result object, 
# which holds the result of running the CLI application with the target arguments and options. 
# Result objects provide several useful attributes and properties, 
# including the application’s exit code and standard output. 
# Take a look at the class documentation for more details.

# Now that you’ve set up the first unit test for your Typer CLI application, 
# you can run the test with pytest. 
# Go back to your command line and execute `python -m pytest tests` from your project’s root directory:



# To test .add(), you must create a Todoer instance with a proper JSON file as the target database. 
# To provide that file, you’ll use a pytest fixture.
# The fixture, mock_json_file(), creates and returns a temporary JSON file, db_file, 
# with a single-item to-do list in it.
# In this fixture, you use tmp_path, which is a pathlib.Path object 
# that pytest uses to provide a temporary directory for testing purposes.
@pytest.fixture
def mock_json_file(tmp_path):
    todo = [{"Description": "Get some milk.", "Priority": 2, "Done": False}]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file

# These two dictionaries (test_data1 and test_data2) provide data to test Todoer.add(). 
test_data1 = {
    # The first two keys represent the data you’ll use as arguments to .add(), 
    "description": ["Clean", "the", "house"],
    "priority": 1,
    # while the third key holds the expected return value of the method.
    "todo": {
        "Description": "Clean the house.",
        "Priority": 1,
        "Done": False,
    },
}
test_data2 = {
    "description": ["Wash the car"],
    "priority": 2,
    "todo": {
        "Description": "Wash the car.",
        "Priority": 2,
        "Done": False,
    },
}

# With pytest, you can use parametrization to provide multiple sets of arguments 
# and expected results to a single test function. This is a pretty neat feature. 
# It makes a single test function behave like several test functions that run different test cases.
# The @pytest.mark.parametrize() decorator marks test_add() for parametrization. 
# When pytest runs this test, it calls test_add() two times. 
# Each call uses one of the parameter sets from lines 91 to 95 and lines 96 to 100.
@pytest.mark.parametrize(
    # This string holds descriptive names for the two required parameters 
    # and also a descriptive return value name. Note that test_add() has those same parameters. 
    # Additionally, the first parameter of test_add() has the same name as the fixture you just defined.
    "description, priority, expected",
    [
        pytest.param(
            test_data1["description"],
            test_data1["priority"],
            (test_data1["todo"], SUCCESS),
        ),
        pytest.param(
            test_data2["description"],
            test_data2["priority"],
            (test_data2["todo"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, description, priority, expected):
    # creates an instance of Todoer with mock_json_file as an argument.
    todoer = mmmap.Todoer(mock_json_file)
    # asserts that a call to .add() using description and priority as arguments should return expected.
    assert todoer.add(description, priority) == expected
    # reads the to-do list from the temporary database and stores it in read.
    read = todoer._db_handler.read_todos()
    # asserts that the length of the to-do list is 2. Why 2? 
    # Because mock_json_file() returns a list with one to-do, and now you’re adding a second one.
    assert len(read.todo_list) == 2