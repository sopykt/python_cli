"""mmmap entry point script."""
# mmmap/__main__.py

from mmmap import cli, __app_name__

# In this function, you call the Typer app with cli.app(), 
# passing the application’s name to the prog_name argument. 
# Providing a value to prog_name ensures that your users get the correct app name 
# when running the --help option on their command line.
def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()