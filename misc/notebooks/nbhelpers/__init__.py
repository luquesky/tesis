import os
import sys

def add_source_path(path=".."):
  sys.path.append(os.path.abspath(path))
