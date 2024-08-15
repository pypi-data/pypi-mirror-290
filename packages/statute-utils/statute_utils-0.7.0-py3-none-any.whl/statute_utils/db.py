import datetime
import logging
from collections.abc import Iterable
from pathlib import Path

from sqlite_utils.db import Database, Table


def add_idx(tbl, cols: Iterable):
    if isinstance(tbl, Table):
        tbl.create_index(
            columns=cols,
            index_name=f"idx_{tbl.name}_{'_'.join(list(cols))}",
            if_not_exists=True,
        )


def add_statute(db: Database, file: Path):
    from .statute import Statute

    if s := Statute.from_file(file=file):
        row = s.make_row()
        fts = row.pop("fts")

        try:
            db["statutes"].insert(record=row, ignore=True)  # type: ignore
        except Exception as e:
            logging.error(f"Could not create statute; {e=}")

        try:
            db["statute_titles"].insert_all(records=s.make_title_rows(), ignore=True)  # type: ignore
        except Exception as e:
            logging.error(f"Could not create statute titles; {e=}")

        try:
            db["statute_units"].insert_all(  # type: ignore
                fts,
                hash_id="id",  # type: ignore
                hash_id_columns=("statute_id", "material_path"),  # type: ignore
                ignore=True,  # type: ignore
            )
        except Exception as e:
            logging.error(f"Could not create statute units; {e=}")


def create_statute_tables(db: Database):
    db["statutes"].create(  # type: ignore
        columns={
            "id": str,
            "cat": str,
            "num": str,
            "date": datetime.date,
            "variant": int,
            "units": str,
            "html": str,
        },
        pk="id",
        defaults={"variant": 1},
        not_null={"cat", "num", "date", "units"},
        if_not_exists=True,
    )
    for idx in (
        {"date"},
        {"cat", "num"},
        {"cat", "num", "date"},
        {"cat", "num", "date", "variant"},
    ):
        add_idx(db["statutes"], idx)

    db["statute_titles"].create(  # type: ignore
        columns={"id": str, "statute_id": str, "cat": str, "text": str},
        pk="id",
        foreign_keys=[("statute_id", "statutes", "id")],
        not_null={"cat", "text"},
        if_not_exists=True,
    )
    add_idx(db["statute_titles"], {"statute_id", "cat"})  # type: ignore

    db["statute_units"].create(  # type: ignore
        columns={
            "id": str,
            "statute_id": str,
            "material_path": str,
            "heading": str,
            "item": str,
            "caption": str,
            "content": str,
            "snippetable": str,
        },
        pk="id",
        foreign_keys=[("statute_id", "statutes", "id")],
        not_null={"statute_id", "material_path"},
        if_not_exists=True,
    )
    for idx in (
        {"material_path"},
        {"statute_id", "material_path"},
    ):
        add_idx(db["statute_units"], idx)


def create_codification_tables(db: Database):
    db["codifications"].create(  # type: ignore
        columns={
            "id": str,
            "cat": str,
            "num": str,
            "title": str,
            "description": str,
            "date": datetime.date,
            "units": str,
            "html": str,
            "is_starter": bool,  # used to signify free use in client
        },
        pk="id",
        not_null={"cat", "num", "title", "description", "date", "units"},
        defaults={"is_starter": False},
        if_not_exists=True,
    )
    for idx in (
        {"date"},
        {"cat", "num"},
        {"cat", "num", "date"},
        {"is_starter"},
    ):
        add_idx(db["codifications"], idx)

    db["codification_units"].create(  # type: ignore
        columns={
            "id": str,
            "codification_id": str,
            "material_path": str,
            "heading": str,
            "item": str,
            "caption": str,
            "content": str,
            "snippetable": str,
        },
        pk="id",
        foreign_keys=[("codification_id", "codifications", "id")],
        not_null={"codification_id", "material_path"},
        if_not_exists=True,
    )
    for idx in (
        {"material_path"},
        {"codification_id", "material_path"},
    ):
        add_idx(db["codification_units"], idx)

    db["codification_statutes"].create(  # type: ignore
        columns={"id": int, "codification_id": str, "statute_id": str},
        pk="id",
        foreign_keys=[
            ("codification_id", "codifications", "id"),
            ("statute_id", "statutes", "id"),
        ],
        not_null={"codification_id", "statute_id"},
        if_not_exists=True,
    )
    for idx in ({"codification_id", "statute_id"},):
        add_idx(db["codification_statutes"], idx)


def add_codification(db: Database, file: Path):
    from .codification import Codification

    starters = ("const-1987", "civil", "penal", "labor", "civpro")
    if c := Codification.from_file(file=file):
        row = c.make_row()
        for starter in starters:
            if starter in row["id"]:
                row["is_starter"] = True

        fts = row.pop("fts")

        try:
            db["codifications"].insert(record=row, ignore=True)  # type: ignore
        except Exception as e:
            logging.error(f"Could not create codifications; {e=}")

        try:
            db["codification_units"].insert_all(  # type: ignore
                fts,
                hash_id="id",  # type: ignore
                hash_id_columns=("codification_id", "material_path"),  # type: ignore
                ignore=True,  # type: ignore
            )
        except Exception as e:
            logging.error(f"Could not create codification units; {e=}")

        events = c.extract_events()
        included_statutes = {evt["statute"] for evt in events if evt.get("statute")}
        db["codification_statutes"].insert_all(  # type: ignore
            records=(
                (
                    {"codification_id": c.slug} | statute_row
                    for text in included_statutes
                    for statute_row in db["statute_titles"].rows_where(
                        where="text = ?",
                        where_args=(text,),
                        select="statute_id",
                    )
                )
            ),
            pk="id",  # type: ignore
        )
