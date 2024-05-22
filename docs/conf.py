""" default sphinx settings
"""
import os
import re
from datetime import datetime
from glob import glob
from os.path import join

from autop import Project, utils


def clean_rst():
    """ cleans up rst before sphinx.
    removes module hierarchy and extra headers
    """
    pattern = r"((?:[a-zA-Z0-9\_]*[.])*([a-zA-Z0-9\_]+) (package|module))"
    for file in glob("_rst/*"):
        with open(file) as f:
            content = f.read()
        content = re.sub(pattern, r"\g<2>", content)
        content = content.replace(f"Submodules\n----------\n\n", "")
        content = content.replace("Module contents\n---------------\n\n", "")
        with open(file, "w") as f:
            f.write(content)
    os.remove("_rst/modules.rst")


clean_rst()

# user
author = utils.get_user()
copyright = ", ".join([str(datetime.now().year), author])

# project
p = Project()
project = p.name()
version = p.version()
# mock missing imports so sphinx can create docs without installing (e.g. for source that runs in a container)
_, _, autodoc_mock_imports = p.imports()

# format
autoclass_content = "both"
html_theme = "sphinx_rtd_theme"
extensions = [
    "sphinx.ext.autodoc",  # source code docstrings
    "sphinx.ext.viewcode",  # link to source code
    "nbsphinx",  # insert views of jupyter notebooks in the docs
]
