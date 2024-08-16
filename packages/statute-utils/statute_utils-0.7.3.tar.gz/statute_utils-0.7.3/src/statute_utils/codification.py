import datetime
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any, NamedTuple

import yaml  # type: ignore
from dateutil.parser import parse  # type: ignore
from rich.progress import track
from sqlite_utils.db import Database, Table

from .components import (
    create_fts_snippet_column,
    create_unit_heading,
    fetch_values_from_key,
    set_node_ids,
)
from .extractor import extract_rule
from .models import Rule
from .templater import html_tree_from_hierarchy
from .utils import add_idx, check_table


class Codification(NamedTuple):
    """A instance is dependent on a specifically
    formatted codification Path, i.e.:

    ```<folder>/<statute-category>/<statute-id>/<specific-code-id>`

    The shape of the contents will be different
    from the shape of the dumpable `.yml` export."""

    title: str
    description: str
    date: datetime.date
    slug: str
    rule: Rule
    units: list[dict]

    def __str__(self) -> str:
        return f"code: {self.rule.__str__()}, {self.date.strftime('%b %d, %Y')}"

    def __repr__(self) -> str:
        return "/".join([self.rule.cat.value, self.rule.num, self.slug])

    @classmethod
    def from_file(cls, file: Path):
        data = yaml.safe_load(file.read_bytes())

        base = data.get("base")
        if not base:
            return None

        rule = extract_rule(base)
        if not rule:
            return None

        title = data.get("title")
        if not title:
            return None

        description = data.get("description")
        if not description:
            return None

        dt = data.get("date")
        if not dt:
            return None

        return cls(
            title=title,
            description=description,
            date=parse(dt).date(),
            slug=file.stem,
            rule=rule,
            units=data.get("units"),
        )

    def prepare_root(self):
        """Adds material paths to each node in the tree with the root
        node given special features: it's marked with a material path `id`
        of `1.`"""
        set_node_ids(self.units)
        root = {"id": "1.", "units": self.units}
        return [root]

    def make_row(self) -> dict:
        """See same logic in Statute."""
        units = self.prepare_root()
        fts = self.flatten_units(self.slug, units)  # excludes the root
        html = html_tree_from_hierarchy(units[0]["units"])  # excludes root
        return {
            "id": self.slug,
            "title": self.title,
            "description": self.description,
            "cat": self.rule.cat.value,
            "num": self.rule.num,
            "date": self.date,
            "units": units,
            "fts": fts,
            "html": html,
        }

    @classmethod
    def flatten_units(
        cls, codification_id: str, units: list[dict[str, Any]], heading: str = ""
    ) -> Iterator[dict[str, str | None]]:
        """See same logic in Statute."""
        for unit in units:
            present_heading = create_unit_heading(unit, heading)
            yield {
                "codification_id": codification_id,
                "material_path": unit["id"],  # enable subtree
                "heading": present_heading,  # identify subtree
                "item": unit.get("item"),
                "caption": unit.get("caption"),
                "content": unit.get("content"),
                "snippetable": create_fts_snippet_column(unit),  # enable searchability
            }
            if subunits := unit.get("units"):
                yield from cls.flatten_units(codification_id, subunits, present_heading)

    def extract_events(self) -> Iterator[dict]:
        """Each unit in a codification may contain a history.

        To ensure that strings do not contain miscellaneous content, this runs a
        check on each event key prior to yielding the event.
        """
        data = {"units": self.units}
        histories = fetch_values_from_key(data=data, key="history")
        for history in histories:
            for event in history:
                for key, value in event.items():
                    if isinstance(value, str):
                        event[key] = value.strip()
                yield event

    @classmethod
    def create_composition_table(cls, db: Database) -> Table:
        """Each `Codification` consists of various `Statutes`"""
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

        return check_table(db["codification_statutes"])

    @classmethod
    def create_root_table(cls, db: Database) -> Table:
        """Each `Codification` is a container tree renderable via
        its `html` property."""
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

        return check_table(db["statutes"])

    @classmethod
    def create_units_table(cls, db: Database) -> Table:
        """Every `Codification` contains branches called units."""
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

        return check_table(db["statute_units"])

    @classmethod
    def add_row(cls, db: Database, file: Path):
        """Each `Codification` originating from a `file` can be converted
        into a database row that will fill up the tables created
        in `cls.create_root_table()` and `cls.create_units_table()`.

        Args:
            db (Database): Contains tables created by `cls.create_root_table()`
                and `cls.create_units_table()`
            file (Path): `*.yml` file that is the source of truth for the
                `Statute` record.
        """
        code = cls.from_file(file=file)
        if not code:
            raise ValueError(f"Could not create Codification from {file=}")

        row = code.make_row()
        fts = row.pop("fts")

        starters = ("const-1987", "civil", "penal", "labor", "civpro")
        for starter in starters:
            if starter in row["id"]:
                row["is_starter"] = True

        try:
            db["codifications"].insert(record=row, ignore=True)  # type: ignore
        except Exception as e:
            raise ValueError(f"Could not create codification; {e=}")

        try:
            db["codification_units"].insert_all(  # type: ignore
                fts,
                hash_id="id",  # type: ignore
                hash_id_columns=("codification_id", "material_path"),  # type: ignore
                ignore=True,  # type: ignore
            )
        except Exception as e:
            raise ValueError(f"Could not create codification units; {e=}")

        events = code.extract_events()
        included_statutes = {evt["statute"] for evt in events if evt.get("statute")}
        db["codification_statutes"].insert_all(  # type: ignore
            records=(
                (
                    {"codification_id": code.slug} | statute_row
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

    @classmethod
    def source(cls, db_name: str, folder: str, pattern: str):
        """Initializes codification from source *.yml files.

        Args:
            db_name (str): Name of the database file to use.
            folder (str): Where the *.yml files are found.
            pattern (str): What glob pattern to use to detect the yml files.
        """
        db = Database(filename_or_conn=db_name, use_counts_table=True)
        root_table = cls.create_root_table(db)
        units_table = cls.create_units_table(db)
        _ = cls.create_composition_table(db)
        files = list(Path(folder).glob(pattern))
        for file in track(files, description="Codification files..."):
            try:
                cls.add_row(db=db, file=file)
            except Exception as e:
                logging.error(f"Codification from {file=}; {e=}")
        # fts
        units_table.enable_fts(["snippetable"], replace=True)
        root_table.enable_fts(["title", "description"], replace=True)
        # finalize
        db.index_foreign_keys()
        db.vacuum()
