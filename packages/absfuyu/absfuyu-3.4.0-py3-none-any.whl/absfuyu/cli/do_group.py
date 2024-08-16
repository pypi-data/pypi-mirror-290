"""
ABSFUYU CLI
-----------
Do

Version: 1.1.0
Date updated: 15/08/2024 (dd/mm/yyyy)
"""

__all__ = ["do_group"]

import subprocess

import click

from absfuyu import __title__
from absfuyu.cli.color import COLOR
from absfuyu.core import __package_feature__
from absfuyu.general.human import Human2
from absfuyu.version import PkgVersion


@click.command()
@click.option(
    "--force_update/--no-force-update",
    "-F/-f",
    "force_update",
    type=bool,
    default=True,
    show_default=True,
    help="Update the package",
)
def update(force_update: bool) -> None:
    """Update the package to latest version"""
    click.echo(f"{COLOR['green']}")
    AbsfuyuPackage = PkgVersion(
        package_name=__title__,
    )
    AbsfuyuPackage.check_for_update(force_update=force_update)


@click.command()
@click.argument("pkg", type=click.Choice(__package_feature__))
def install(pkg: str) -> None:
    """Install absfuyu's extension"""
    cmd = f"pip install -U absfuyu[{pkg}]".split()
    try:
        subprocess.run(cmd)
    except Exception:
        try:
            cmd2 = f"python -m pip install -U absfuyu[{pkg}]".split()
            subprocess.run(cmd2)
        except Exception:
            click.echo(f"{COLOR['red']}Unable to install absfuyu[{pkg}]")
        else:
            click.echo(f"{COLOR['green']}absfuyu[{pkg}] installed")
    else:
        click.echo(f"{COLOR['green']}absfuyu[{pkg}] installed")


@click.command()
def advice() -> None:
    """Give some recommendation when bored"""
    from absfuyu.fun import im_bored

    click.echo(f"{COLOR['green']}{im_bored()}")


@click.command(name="fs")
@click.argument("date", type=str)
@click.argument("number_string", type=str)
def fs(date: str, number_string: str) -> None:
    """Feng-shui W.I.P"""

    instance = Human2(date)
    print(instance.fs(number_string))


@click.command(name="info")
@click.argument("date", type=str)
def info(date: str) -> None:
    """Day info"""

    instance = Human2(date)
    print(instance.info())


@click.group(name="do")
def do_group() -> None:
    """Perform functionalities"""
    pass


do_group.add_command(update)
do_group.add_command(install)
do_group.add_command(advice)
do_group.add_command(fs)
do_group.add_command(info)
