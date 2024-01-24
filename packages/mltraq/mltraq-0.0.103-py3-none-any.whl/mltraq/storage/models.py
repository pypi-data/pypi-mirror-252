from sqlalchemy import BigInteger, Column, LargeBinary, String
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types.uuid import UUIDType

from mltraq import options

# Construct a base class for declarative class definitions.
Base = declarative_base()

# UUID type, to be used in model definitions. By passing binary=False, we fall back
# to the string representation of UUIDs if there's no native type (as in SQLite).
# Why string? falling back on binary complicates direct SQL queries.
uuid_type = UUIDType(binary=False)


class Experiment(Base):
    """Model representing the index record of an experiment in the database."""

    # TODO: use a class property to eval the value of the option.
    __tablename__ = options.get("db.experiments_tablename")
    id_experiment = Column(uuid_type, primary_key=True, default=None)
    name = Column(String, nullable=False, unique=True)
    runs_size = Column(BigInteger, nullable=False, default=None)
    runs_meta = Column(LargeBinary, nullable=True, default=None)
    fields = Column(LargeBinary, nullable=False, default=None)
    pickle = Column(LargeBinary, nullable=True, default=None)
