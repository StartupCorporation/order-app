import os
from pathlib import Path

from invoke.tasks import task
from invoke.context import Context


@task
def _change_to_root_dir(*_):
    """
    Internal pre-task to change working directory to the root directory of the project.
    """
    os.chdir(Path(__file__).parent.parent)


@task(
    name="sync-kernel",
    pre=[_change_to_root_dir],
)
def sync_shared_kernel(
    context: Context,
):
    """
    Installs local shared kernel to the virtual environment.
    """
    context.run("pip install -q ../../dw_shared_kernel")
    context.run("rm -r ../../dw_shared_kernel/src/dw_shared_kernel.egg-info")
    context.run("rm -r ../../dw_shared_kernel/build")
    print("Installed local shared kernel to the virtual environment.")


@task(
    name="compile",
    help={
        "extra": "The additional packages section to install.",
        "output_file": (
            "The output file where compiled packages will be written.Default is 'requirements/requirements.local.txt'."
        ),
    },
    optional=["extra"],
    pre=[_change_to_root_dir],
)
def compile_(
    context: Context,
    extra: str | None = None,
    output_file: str = "requirements/requirements.local.txt",
) -> None:
    """
    Compiles packages from the pyproject.toml file to the output file.
    """
    args = [
        "-q",
        f"-o {output_file}",
        "--no-header",
        "--no-annotate",
        "--no-strip-extras",
        "pyproject.toml",
    ]

    if extra:
        args.insert(0, f"--extra {extra}")

    context.run(f"pip-compile {' '.join(args)}")
    context.run("rm -rf src/order_app.egg-info")
    print(f"Successfully compiled packages to the '{output_file}'.")


@task(
    help={
        "packages": "The list of packages to upgrade. Must be separeted by whitespace.",
        "output_file": (
            "The output file where compiled packages will be written.Default is 'requirements/requirements.local.txt'."
        ),
    },
    pre=[_change_to_root_dir],
)
def upgrade(
    context: Context,
    packages: str,
    output_file: str = "requirements/requirements.local.txt",
) -> None:
    """
    Upgrades packages that are specified in the args and writes new packages' version to specified file.
    """
    packages_list = packages.split()
    args = [
        "-q",
        f"-o {output_file}",
        "--no-header",
        "--no-annotate",
        "--no-strip-extras",
        *map(lambda package: f"--upgrade-package {package}", packages_list),
        "pyproject.toml",
    ]
    context.run(f"pip-compile {' '.join(args)}")
    context.run("rm -rf src/order_app.egg-info")
    print(
        f"Upgraded {' '.join(packages_list)} {'packages' if len(packages_list) > 1 else 'package'}"
        f"to the {output_file} file.",
    )


@task(
    help={
        "file": "The file containing the packages to install. Default is 'requirements/requirements.local.txt'.",
    },
    pre=[_change_to_root_dir],
)
def install(
    context: Context,
    file: str = "requirements/requirements.local.txt",
) -> None:
    """
    Install packages from the provided requirements file.
    """
    context.run(f"pip-sync {file} -q")
    print(f"Successfully installed packages from the '{file}'.")
