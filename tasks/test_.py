from dw_python_clis import change_to_root_dir
from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task


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
    context.run(
        "source ../infrastructure/.env.local.test && pytest src/",
        pty=True,
    )


collection = Collection(
    run_tests,
)
