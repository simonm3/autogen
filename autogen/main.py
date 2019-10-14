#!/usr/bin/env python
try:
    import win32api
except:
    # not available on linux
    pass
from docopt import docopt
import shutil
import subprocess
import shlex
from glob import glob
import os
from .default_conf import ignore_folders

HERE = os.path.abspath(os.path.join(__file__, os.pardir))

def main():
    """
    Zero configuration to create and publish html documentation

    Installation::

        pip install docopt nbsphinx pipreqs sphinx sphinx-rtd-theme win32api
        conda install -c conda-forge docopt nbsphinx pipreqs sphinx sphinx-rtd-theme win32api

    Usage:
        ./conf.py index
        ./conf.py (rst|html)...

    options:
      -h, --help  Display this help message

    commands:
      index Create a starter version of index.rst for editing
      rst   Create rst docstrings in docs/_rst
      html  Create html docs in docs/_build/html

    To automatically create and publish docs every commit see ".gitlab-ci.yml"

    todo run from docs or root folder
    """
    opts = docopt(main.__doc__)

    if opts["index"]:
        create_index()
        return

    if opts["rst"]:
        shutil.rmtree("_rst", ignore_errors=True)
        for path in [os.path.abspath(x).replace("\\", "/") for x in glob("../*")]:
            if os.path.basename(path) in ignore_folders:
                continue
            cmd = shlex.split(f"sphinx-apidoc -f {path} -o _rst")
            subprocess.run(cmd)

    if opts["html"]:
        shutil.rmtree("_build", ignore_errors=True)
        if "index.rst" not in os.listdir("."):
            raise Exception("run './conf.py index' or create index.rst manually before building html")
        cmd = shlex.split(f"sphinx-build -M html . _build")
        subprocess.run(cmd)


def create_index():
    """ create index.rst using existing files or example data """
    global packages
    if "index.rst" in os.listdir("."):
        raise Exception("there is already an index.rst file. delete the old one if you want to recreate")
    chapters = list(glob("*.rst") + glob("*.ipynb"))
    chapters = chapters or ["chapter1.rst", "chapter2.rst"]
    chapters = [chapter[:-4] if chapter.endswith(".rst") else chapter for chapter in chapters]
    chapters = "\n".join([f"   {chapter}" for chapter in chapters])
    packages = packages or ["package1", "package2"]
    packages = "\n".join([f"   _rst/{pack}" for pack in packages])
    with open(f"{HERE}/default_index.rst") as f:
        index = f.read()
    index = index.format(chapters=chapters, packages=packages)
    with open("index.rst", "w") as f:
        f.write(index)

if __name__ == "__main__":
    main()
