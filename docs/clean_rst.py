import re
from glob import glob


def clean_rst():
    """ cleans up rst before sphinx.
    removes module hierarchy and extra headers
    """
    pattern = "((?:[a-zA-Z0-9\\_]*[.])*([a-zA-Z0-9\\_]+) (package|module))"
    for file in glob("_rst/*"):
        with open(file) as f:
            content = f.read()
        content = re.sub(pattern, "\g<2>", content)
        content = content.replace(f"Submodules\n----------\n\n", "")
        content = content.replace("Module contents\n---------------\n\n", "")
        with open(file, "w") as f:
            f.write(content)


if __name__ == "__main__":
    clean_rst()
