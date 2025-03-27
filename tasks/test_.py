from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task

from tasks.shared import change_to_root_dir


@task(
    name="run",
    pre=[change_to_root_dir],
)
def run_tests(
    context: Context,
):
    """
    Runs tests.
    """
    context.run("pytest src/", pty=True)


collection = Collection(
    run_tests,
)
