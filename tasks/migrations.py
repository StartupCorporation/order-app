from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task

from tasks.shared import change_to_root_dir


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
    context.run("cd src/infrastructure/database/relational/migrations && yoyo new")
    context.run("rm -rf src/infrastructure/database/relational/migrations/__pycache__")


collection = Collection(
    create_new_migration,
)
