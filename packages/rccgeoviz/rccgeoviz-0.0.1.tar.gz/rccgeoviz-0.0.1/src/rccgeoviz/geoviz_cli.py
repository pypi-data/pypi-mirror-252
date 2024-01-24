import subprocess
import argparse
import sys


# def run_panel_tool():
#    subprocess.run(
#        [
#            "jupyter",
#            "nbconvert",
#            "--execute",
#            "--to",
#            "notebook",
#            "--inplace",
#            "docs/panel/panel_tool.ipynb",
#        ]
#    )


def main(argv=None):
    """argv is an array of strings, simulating command line arguments"""
    parser = argparse.ArgumentParser(
        description="Command-Line Interface for GeoViz Project"
    )
    # https://docs.python.org/3/library/argparse.html#action
    parser.add_argument(
        "--options",
        help="File path to the JSON configuration folder",
        metavar="filename",
    )

    args = parser.parse_args(argv)
    print("arguments:", args)


if __name__ == "__main__":
    sys.exit(main())

"""
We use subprocess.run to call the jupyter nbconvert command, which can execute a Jupyter notebook from the command line. Adjust the path to the notebook accordingly.
The --inplace flag modifies the notebook in place, so you don't have to worry about creating additional files.
The --execute flag ensures that the notebook is executed.

Now, you can run the panel_tool.ipynb from the command line using:
python cli/geoviz_cli.py --run-panel-tool

Run from the root directory 
"""
