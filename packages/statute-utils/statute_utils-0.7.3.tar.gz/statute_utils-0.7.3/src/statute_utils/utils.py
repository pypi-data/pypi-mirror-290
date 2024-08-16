from collections.abc import Iterable

from sqlite_utils.db import Table


def check_table(tbl) -> Table:
    if isinstance(tbl, Table):
        return tbl
    raise ValueError("Must be a valid table.")


def add_idx(tbl, cols: Iterable):
    if isinstance(tbl, Table):
        tbl.create_index(
            columns=cols,
            index_name=f"idx_{tbl.name}_{'_'.join(list(cols))}",
            if_not_exists=True,
        )
