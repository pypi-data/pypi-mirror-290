"""Module supports dataclass storage and retrieval."""
from dataclasses import dataclass
import pickle

from membank.datamethods import create_table, get_item, update_item


@dataclass
class TableClass():
    """Maps a dataclass to a Table."""

    table: str = ""
    classload: bytes = b""


class Mapper():
    """Interface to store and retrieve dataclasses."""

    def __init__(self, engine, metadata):
        """Initialise."""
        self.engine = engine
        if "__meta_dataclasses__" not in metadata:
            create_table("__meta_dataclasses__", TableClass(), self.engine)
            metadata.reflect(bind=self.engine)
        self.sql_table = metadata.tables["__meta_dataclasses__"]

    def get_class(self, table):
        """Return dataclass representing table."""
        table_class = get_item(
            self.sql_table,
            self.engine,
            TableClass,
            **{"table": table}
        )
        if table_class:
            return pickle.loads(table_class.classload)
        return None

    def put_class(self, table, table_class):
        """Store dataclass representing table."""
        classload = pickle.dumps(table_class)
        update_item(
            self.sql_table,
            self.engine,
            TableClass(table=table, classload=classload),
            key="table"
        )
