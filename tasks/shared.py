import os
from pathlib import Path

from invoke.tasks import task


@task
def change_to_root_dir(*_):
    """
    Internal pre-task to change working directory to the root directory of the project.
    """
    os.chdir(Path(__file__).parent.parent)
