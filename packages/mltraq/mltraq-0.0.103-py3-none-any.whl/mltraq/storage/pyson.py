import json
import uuid
import zlib

import numpy as np
import pandas as pd

# Dictionaries are decoded as Bunch classes. You can substitute Bunch with
from mltraq.utils.bunch import Bunch

# Keyword used to identify serialized values and the version of the serialization format.
MAGIC_KEY = "PYJSON-type-0.0"

# Types that are handled by serialization.
SERIALIZED_TYPES = [pd.DataFrame, pd.Series, np.ndarray, uuid.UUID, dict, tuple, list, tuple]


def compress(data: bytes, enable_compression=False) -> bytes:
    """Compress a sequence of bytes.

    Args:
        data (bytes): Data to compress.
        enable_compression (_type_, optional): Force compression (enable/disable)
            regardless the default. Defaults to None.

    Returns:
        bytes: Compressed data.
    """

    if enable_compression:
        return zlib.compress(data)
    else:
        return data


def decompress(data: bytes) -> bytes:
    """Decompress the data. It works also with uncompressed data: if zlib fails,
        it returns the input data.

    Args:
        data (bytes): Data to decompress.

    Returns:
        bytes: Decompressed data.
    """
    if isinstance(data, memoryview):
        data = data.tobytes()

    try:
        data = zlib.decompress(data)
    except zlib.error:
        pass

    return data


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        """Return the dictionary that represents the serialized version of an object

        Args:
            obj (_type_): Object to serialize

        Returns:
            _type_: dict containing the serialized object
        """

        if isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series):
            # Since, in presence of timestamps in either columns or index, we're going to change the data,
            # let's work on a copy of the dataframe to not modify the original dataframe.
            # If it's a series, we just convert it to a dataframe, implicitly obtaining a copy of the data.
            if isinstance(obj, pd.Series):
                obj = obj.to_frame()
                obj_type = "pandas.Series-0.0"
            else:
                obj = obj.copy()
                obj_type = "pandas.DataFrame-0.0"

            dtypes = {col: str(obj[col].dtype) for col in obj.columns}
            dtype_index = str(obj.index.dtype)

            # handle timestamps serialization in columns
            cols_datetime64ns = [col for col in obj.columns if obj[col].dtype == "datetime64[ns]"]
            if len(cols_datetime64ns) > 0:
                # some columns contain timestamps, let's convert them to strings
                for col in cols_datetime64ns:
                    obj[col] = obj[col].astype(int)

            # Timestamps in the index have a dtype "<M8[ns]" instead of "datetime64[ns]" (not sure why
            # it's nost simply "datetime64[ns]" as for columns).  This is why we catch multiple dtype
            # types that might be associated to timestamps.
            if dtype_index in ["<M8[ns]", ">M8[ns]", "datetime64[ns]"]:
                obj.index = obj.index.astype(int)

            return {
                MAGIC_KEY: obj_type,
                "dtype-index": dtype_index,
                "dtypes": dtypes,
                "data": obj.to_dict(orient="list"),
                "index": obj.index.tolist(),
            }
        elif isinstance(obj, np.ndarray):
            return {MAGIC_KEY: "numpy.ndarray-0.0", "data": obj.tolist(), "dtype": obj.dtype.name}
        elif isinstance(obj, uuid.UUID):
            return {MAGIC_KEY: "uuid.UUID-0.0", "data": str(obj)}
        else:
            return json.JSONEncoder.default(self, obj)


def serialize(obj: object, enable_compression=False) -> bytes:
    """Serialize an object

    Args:
        obj (object): Object to serialize
        enable_compression (_type_, optional): If not None, enable/disable compression.
            If None, consider default preference. Defaults to None.

    Returns:
        bytes: Serialized object.
    """

    return compress(json.dumps(obj, cls=JSONEncoder).encode("UTF-8"), enable_compression=enable_compression)


def deserialize(obj: bytes) -> object:  # noqa
    """Deserialize an object

    Args:
        obj (bytes): Object to deserialize.

    Returns:
        object: Unserialized object.
    """
    if isinstance(obj, memoryview):
        obj = obj.tobytes()

    def f(v):
        if isinstance(v, dict) and MAGIC_KEY in v:
            # This ia a value to deserialize
            if v[MAGIC_KEY] in ["pandas.DataFrame-0.0", "pandas.Series-0.0"]:
                df = pd.DataFrame.from_dict(v["data"], orient="columns")
                df.index = pd.Index(v["index"]).astype(v["dtype-index"])
                for col, dtype in v["dtypes"].items():
                    df[col] = df[col].astype(dtype)
                if v[MAGIC_KEY] == "pandas.DataFrame-0.0":
                    return df
                else:
                    # Return first column, a series
                    return df[df.columns[0]]
            elif v[MAGIC_KEY] == "numpy.ndarray-0.0":
                return np.asarray(v["data"], dtype=v["dtype"])
            elif v[MAGIC_KEY] == "uuid.UUID-0.0":
                return uuid.UUID(v["data"])
            else:
                # We don't know how to deserialize it, return it as a dictionary.
                return Bunch(v)
        elif isinstance(v, list):
            # Walk thru the list, trying to decode values.
            return [f(v) for v in v]
        elif isinstance(v, tuple):
            # Walk thru the tuple, trying to decode values.
            return [f(v) for v in v]
        elif isinstance(v, dict):
            # Walk thru the dict, trying to decode values.
            return Bunch({kv[0]: f(kv[1]) for kv in v.items()})
        else:
            # Nothing to do, return value.
            return v

    return json.loads(decompress(obj).decode("UTF-8"), object_hook=f)
