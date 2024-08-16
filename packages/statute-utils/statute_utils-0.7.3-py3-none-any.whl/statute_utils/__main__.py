from pathlib import Path

import click
from sqlite_utils import Database

from .config import setup_local_statute_db


@click.group()
def cli():
    """Wrapper of commands for statute-utils."""
    pass


@cli.command()
@click.option(
    "--folder",
    default="../corpus-statutes",
    required=True,
    help="Location of raw files to create database",
)
def interim_db(folder: str):
    """Create interim statute database."""
    setup_local_statute_db(Path(folder))


@cli.command()
@click.option("--db-name", default="rules.db", help="Filename of db")
def source(db_name: str) -> Database:
    """Prepare existing db path by first deleting it creating a new one in WAL-mode.

    Args:
        db_name (str): e.g. "x.db", or "data/main.db"

    Returns:
        Database: The configured database object.
    """
    if not db_name.endswith((".sqlite", ".db")):
        raise ValueError("Expects either an *.sqlite, *.db suffix")

    _db_file = Path(db_name)
    _db_file.unlink(missing_ok=True)

    db = Database(filename_or_conn=_db_file, use_counts_table=True)
    db.enable_wal()
    return db


@cli.command()
@click.option("--db-name", default="my.db", help="Filename of db")
@click.option("--folder", default="../corpus-statutes", help="*.yml files")
@click.option("--pattern", default="**/*/*.yml", help="Glob pattern within --folder")
def source_statutes(db_name: str, folder: str, pattern: str):
    """Initializes statutes from source *.yml files."""
    from .statute import Statute

    Statute.source(db_name=db_name, folder=folder, pattern=pattern)


@cli.command()
@click.option("--db-name", default="my.db", help="Filename of db")
@click.option("--folder", default="../corpus-codifications", help="*.yml files")
@click.option("--pattern", default="**/*/*.yml", help="Glob pattern within --folder")
def source_codifications(db_name: str, folder: str, pattern: str):
    """Initializes codifications from source *.yml files."""
    from .codification import Codification

    Codification.source(db_name=db_name, folder=folder, pattern=pattern)


if __name__ == "__main__":
    cli()
