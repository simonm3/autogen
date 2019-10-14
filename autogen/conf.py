#!/usr/bin/env python
import sys
from os.path import join, basename
from datetime import datetime

try:
    import win32api
except:
    # not available on linux
    pass
from pipreqs import pipreqs
import importlib
from glob import glob
import os

#####################
# Project information
#####################

# author from username
try:
    # windows full name
    author = win32api.GetUserNameEx(3)
except:
    # gitlab CI full name of user that started the job
    author = os.environ.get("GITLAB_USER_NAME", "")

# project name from root folder
copyright = ", ".join([str(datetime.now().year), author])
root = os.path.abspath(join(__file__, os.pardir, os.pardir))
project = basename(root)

# version from first <version.py>.__version__
try:
    versionfiles = glob(f"{root}/**/version.py", recursive=True)
    sys.path.insert(0, os.path.abspath(os.path.join(versionfiles[0], os.pardir)))
    version = importlib.__import__("version").__version__
except:
    version = "latest"

########
# source
########

# ignore these folders
ignore_folders = ["nbs", "docs", "models", "_rst"
                                           ".hg", ".svn", ".git", ".tox",
                  "__pycache__",
                  "env", "venv"]

# enable sphinx to import packages as they may not be installed
packages = []
for d in [d for d in glob(f"{root}/*") if os.path.isdir(d)]:
    if os.path.basename(d) in ignore_folders or d in sys.path:
        continue
    sys.path.insert(0, d)
    packages.append(os.path.basename(d))

# mock all imports that are not installed so project packages can be imported without errors
imports = pipreqs.get_all_imports(root, extra_ignore_dirs=ignore_folders)
autodoc_mock_imports = [f for f in imports if importlib.util.find_spec(f) is None]

# concatenates docstrings for class and __init__
autoclass_content = 'both'

########
# layout
########

# same as python. better than the default theme.
html_theme = 'sphinx_rtd_theme'

# includes the todos in the docs
todo_include_todos = True

# use these for changing default layout e.g. adding comments using disqus
# templates_path = ['_templates']
# html_static_path = ['_static']

############
# extensions
############

extensions = [
    'sphinx.ext.autodoc',  # automatically include docstrings
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',  # enable todo boxes
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',  # insert links to source code
    'sphinx.ext.githubpages',
    'nbsphinx'  # insert views of jupyter notebooks in the docs
]
# maps links to docs for other packages
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
