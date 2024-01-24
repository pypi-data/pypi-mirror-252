from joblib.parallel import DEFAULT_BACKEND

from mltraq.utils.options import BaseOptions

default_options = {
    "reproducibility": {"random_seed": 123, "fake_incremental_uuids": False},
    "db": {
        "url": "sqlite:///:memory:",
        "echo": False,
        "pool_pre_ping": True,
        "ask_password": False,
        "query_read_chunk_size": 1000,
        "query_write_chunk_size": 1000,
        "experiments_tablename": "experiments",
        "experiment_tableprefix": "experiment_",
    },
    "execution": {
        "exceptions": {"compact_message": False},
        "backend": DEFAULT_BACKEND,
        "n_jobs": -1,
    },
    "tqdm": {"disable": False, "delay": 0, "leave": False},
    "serialization": {
        "enable_compression": False,
        "store_pickle": False,
    },
    "dask": {
        "scheduler_address": "tcp://127.0.0.1:8786",
        "dashboard_address": ":8787",
        "scheduler_port": 8786,
        "client_timeout": "5s",
    },
    "app": {},
}


class Options(BaseOptions):
    default_options = default_options


# This object handles the options for the package, process-wide.
# In case of parallel execution, options are propagated to the processes running steps.
# To change locally the preferences, use ctx.
options = Options.instance()

# Other project constants
doc_url = "https://www.mltraq.com"
