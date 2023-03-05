# tests/test_mmmap.py

# imports CliRunner from typer.testing.
from typer.testing import CliRunner

# imports a few required objects from your mmmap package.
from mmmap import __app_name__, __version__, cli

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