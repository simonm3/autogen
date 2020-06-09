import logging
import os
import shutil
from pathlib import Path

import pytest

log = logging.getLogger()


@pytest.fixture(scope="session", autouse=True)
def chdir():
    """ run in test folder """
    curr = os.getcwd()
    os.chdir(Path(__file__).parent)
    yield
    os.chdir(curr)


@pytest.fixture
def tmp_path(tmp_path):
    """ temporary path within test folder to avoid excessively long windows path """
    return Path("/".join(tmp_path.parts[-2:]))


@pytest.fixture(scope="session")
def tmp_file():
    """ temp file name """
    return "temp1345736"
