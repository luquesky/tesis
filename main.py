"""Main program

Usage:
  main.py file <name>...

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Tesis 0.0.1')
    print(arguments)