import logging
from pathlib import Path

import click
from rich.progress import track
from sqlite_utils import Database

from .config import setup_local_statute_db
from .db import (
    add_codification,
    add_statute,
    create_codification_tables,
    create_statute_tables,
)


@click.group()
def cli():
    """Wrapper of commands for statute-utils."""
    pass


def set_db(db_name: str) -> Database:
    _db_file = Path(db_name)
    _db_file.unlink(missing_ok=True)
    db = Database(filename_or_conn=_db_file, use_counts_table=True)
    db.enable_wal()
    return db


@cli.command()
@click.option("--db-name", default="rules.db", help="Filename of db")
@click.option("--folder", default="../corpus-statutes", help="*.yml files")
@click.option("--pattern", default="**/*/*.yml", help="Glob pattern within --folder")
def source_statutes(db_name: str, folder: str, pattern: str):
    """Initializes statutes from source *.yml files."""
    db = set_db(db_name)
    create_statute_tables(db)
    for file in track(
        list(Path(folder).glob(pattern)), description="Statute tables..."
    ):
        try:
            add_statute(db=db, file=file)
        except Exception as e:
            logging.error(f"Statute from {file=}; {e=}")
    # fts
    db["statute_units"].enable_fts(["snippetable"], replace=True)
    db["statute_titles"].enable_fts(["text"], replace=True)
    # finalize
    db.index_foreign_keys()
    db.vacuum()


@cli.command()
@click.option("--db-name", default="rules.db", help="Filename of db")
@click.option("--folder", default="../corpus-codifications", help="*.yml files")
@click.option("--pattern", default="**/*/*.yml", help="Glob pattern within --folder")
def source_codifications(db_name: str, folder: str, pattern: str):
    """Initializes codifications from source *.yml files."""
    db = Database(filename_or_conn=db_name, use_counts_table=True)
    create_codification_tables(db)
    for file in track(
        list(Path(folder).glob(pattern)), description="Codification tables..."
    ):
        try:
            add_codification(db=db, file=file)
        except Exception as e:
            logging.error(f"Codification from {file=}; {e=}")
    # fts
    db["codification_units"].enable_fts(["snippetable"], replace=True)
    db["codifications"].enable_fts(["title", "description"], replace=True)
    # finalize
    db.index_foreign_keys()
    db.vacuum()


@cli.command()
@click.option(
    "--folder",
    default="../corpus-statutes",
    required=True,
    help="Location of raw files to create database",
)
def init_db(folder: str):
    """Create interim statute database."""
    setup_local_statute_db(Path(folder))


if __name__ == "__main__":
    cli()
