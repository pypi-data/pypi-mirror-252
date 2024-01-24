from functools import partial

import cloudpickle
import pandas as pd

from mltraq import options
from mltraq.storage.pyson import SERIALIZED_TYPES, compress, decompress, serialize
from mltraq.utils.frames import json_normalize

# Introduced with Python 3.8, https://peps.python.org/pep-0574/
# Unpickling might fail: on different architectures, different python version, in case of missing packages.
PICKLE_DEFAULT_PROTOCOL = 5


def pickle_dumps(obj: object) -> bytes:
    """It returns the compressed (zlib) pickled object. The Pickle DEFAULT_PROTOCOL is used
    for maximum compatibility.

    Args:
        obj (object): Object to serialize.

    Returns:
        bytes: Compressed serialized object.
    """

    data = cloudpickle.dumps(obj, protocol=PICKLE_DEFAULT_PROTOCOL)
    data = compress(data, options.get("serialization.enable_compression"))
    return data


def pickle_loads(data: bytes) -> object:
    """It returns the loaded object, afer uncompressing and unpickling it.

    Args:
        data (bytes): Serialized object.

    Returns:
        object: Unserialized object.
    """
    return cloudpickle.loads(decompress(data))


def pickle_size(obj: object, unit: str = "b") -> int:
    """It returns the size of the object once serialised (including compression).

    Args:
        obj (object): Object to analyse.
        unit (str, optional): Unit of measure, b (Bytes), kb (KiloBytes), mb (MegaBytes). Defaults to "b".

    Returns:
        int: Size of the serialized object.
    """
    size_object = len(pickle_dumps(obj))
    if unit == "b":
        return size_object
    elif unit == "kb":
        return int(size_object / (2**10) * 1e2) / 1e2
    elif unit == "mb":
        return int(size_object / (2**20) * 1e2) / 1e2
    else:
        return None


def serialize_df(df: pd.DataFrame, ignore_columns: list = None, enable_compression=None):
    """Serialize some of the columns of the dataframe, making it ready for database storage.

    Args:
        df (pd.DataFrame): Dataframe to process.
        ignore_columns (list, optional): Columns to ignore. Defaults to None.
        enable_compression (_type_, optional): If not None, force enable/disable of compression. Defaults to None.

    Returns:
        _type_: _description_
    """

    enable_compression = options.default_if_null(enable_compression, "serialization.enable_compression")

    consider_columns = [col_name for col_name in df.columns if col_name not in ignore_columns]

    # Identify columns to serialize
    serialized_cols = []
    for col_name in consider_columns:
        for serialized_type in SERIALIZED_TYPES:
            # We assume that the types in the first row are the same of the other rows.
            if isinstance(df[col_name].iloc[0], serialized_type):
                serialized_cols.append(col_name)
                break

    if len(serialized_cols) > 0:
        # If there are columns to serialize, work on a frame deep copy.
        df = df.copy()
        for col_name in serialized_cols:
            df[col_name] = df[col_name].map(partial(serialize, enable_compression=enable_compression))

    # Identify columns that haven't been serialized, among the ones to be considered.
    non_serialized_cols = [col_name for col_name in consider_columns if col_name not in serialized_cols]

    columns = {"serialized": serialized_cols, "non-serialized": non_serialized_cols, "compression": enable_compression}
    return df, columns


def explode_json_column(df: pd.DataFrame, col_name: str, prefix: str = None, suffix: str = None) -> pd.DataFrame:
    """Explode a column in the Pandas dataframe containing a dict to a list of columns.
    Useful to handle the "attributes" column in the "Experiments" table, which contains
    the serialized values as JSON.
    Args:
        df (pd.DataFrame): Pandas dataframe
        col_name (str): Column to process.
        prefix (str, optional): Prefix to consider for all exploded columns.
        suffix (str, optional): In case exploded columns already exist, use this suffix.
        Defaults to _{col_name}.
    Returns:
        pd.DataFrame: Resulting Pandas dataframe.
    """

    if suffix is None:
        suffix = f"_{col_name}"

    # Explode column containing json to multiple columns, in a dataframe.
    df_exploded = json_normalize(df[col_name])

    if prefix is not None:
        df_exploded.columns = [f"{prefix}{col_name}" for col_name in df_exploded.columns]

    return df.drop(columns=[col_name]).merge(
        df_exploded,
        how="left",
        left_index=True,
        right_index=True,
        suffixes=(None, suffix),
    )
