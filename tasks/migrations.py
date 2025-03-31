from dw_python_clis import change_to_root_dir
from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task


@task(
    name="new",
    pre=[change_to_root_dir],
)
def create_new_migration(
    context: Context,
) -> None:
    """
    Creates a new migration file.
    """
    context.run("export PYTHONDONTWRITEBYTECODE=1 && cd src/infrastructure/database/relational/migrations && yoyo new")


collection = Collection(
    create_new_migration,
)
