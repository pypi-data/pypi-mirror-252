import logging
import random
import warnings
from functools import partial
from typing import Callable, List, Union

import numpy as np
import pandas as pd

from mltraq import options as global_options
from mltraq.job import Job
from mltraq.storage.database import next_ulid
from mltraq.utils.bunch import Bunch
from mltraq.utils.exceptions import exception_message
from mltraq.utils.frames import json_normalize, reorder_columns
from mltraq.utils.text import stringify

log = logging.getLogger(__name__)


class RunWarning(UserWarning):
    pass


class RunException(Exception):
    """Exceptions reporting exceptions inside executed run steps."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Runs(dict):
    """Handling of a collection of runs. Implemented as a custom dictionary."""

    def __init__(self, runs=None):
        """Initialise the runs.

        Args:
            runs (_type_, optional): If not None, initialise the runs with this dict of runs. Defaults to None.
        """

        if runs is None:
            runs = []
        elif isinstance(runs, Runs):
            runs = runs.values()

        super().__init__({run.id_run: run for run in runs})

    def add(self, *runs):
        """Add runs to the collection (either a single run, or a collection of runs)."""
        for run in runs:
            if isinstance(run, Run):
                self[run.id_run] = run
            elif isinstance(run, Runs):
                for k, v in run.items():
                    self[k] = v

    def first(self):
        """Return the first run."""
        return self[next(iter(self))]

    def next(self):
        """Generate a new run, add it, and return it.

        Returns:
            _type_: _description_
        """
        run = Run()
        self[run.id_run] = run
        return run

    def df(self, max_level=0):
        """Return a pandas DataFrame representation of the collection of runs.

        Args:
            max_level (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        # Load the dataframe from a dict or list of dicts.

        if len(self) == 0:
            # no runs!
            return pd.DataFrame(columns=["id_run"])

        df = json_normalize([{**run.fields, **{"id_run": run.id_run}} for run in self.values()], max_level=max_level)

        return reorder_columns(df, ["id_run"])

    def execute(
        self,
        steps: Union[Callable, List[Callable]] = None,
        config=None,
        backend=None,
        n_jobs=None,
    ):
        """Execute the runs.

        Args:
            steps (Union[Callable, List[Callable]], optional): List of steps to execute on each run. Defaults to None.
            config (_type_, optional): Fixed parameters associated to each run. Defaults to None.
            backend (_type_, optional): Execution backend to use, by default Loky. Defaults to None.
            n_jobs (int, optional): Number of jobs. Defaults to -1 to maximize parallelization.

        Raises:
            run.exception: _description_
        """

        if len(self) == 0:
            # If no runs are defined and we execute the experiment, a dummy one is created.
            warnings.warn(
                "Attempted to execute an experiment with no runs, adding a run with no parameters and executing it",
                category=RunWarning,
                stacklevel=1,
            )
            self.add(Run())

        tasks = [run.execute_func(steps=steps, config=config, options=global_options) for run in self.values()]

        # randomize order of tasks, so that partial results are more representative
        # of the entire set of runs being executed.
        random.Random(global_options.get("reproducibility.random_seed")).shuffle(tasks)

        executed_runs = Job(tasks, n_jobs=n_jobs, backend=backend).execute()

        # TODO: raise exception as soon as it's encountered, without waiting for all
        # parallel jobs to return. (joblib can return an iterator, this is likely how
        # we can achieve this.)

        # Check for exceptions, and raise first one encountered.
        for run in executed_runs:
            if run.exception is not None:
                raise run.exception

        # Point the runs to new instances that contain the result of the execution.
        for run in executed_runs:
            self[run.id_run] = run

    def _repr_html_(self):
        return f"Runs(keys({len(self)})={stringify(self.keys())})"


class Run:
    """A run represents an instance of the experiment, obtained by
    combining the fixed and variable parameters. The Run objects
    (and the tracked fields)  must be serializable with cloudpickle.
    """

    # Attributes to store and serialize.
    __slots__ = ("id_run", "config", "params", "fields", "vars", "state", "exception", "steps")
    __state__ = ("id_run", "config", "params", "fields", "state", "exception")

    def __init__(
        self,
        id_run: str = None,
        steps: Union[Callable, List[Callable]] = None,
        config: dict = None,
        params: dict = None,
        fields: dict = None,
    ):
        """Create a new run.

        Args:
            id_run: ID of the run.
            steps (Union[Callable, List[Callable]], optional): One or more functions to be executed. Their
            config (dict, optional): Fixed parameters for all runs of an experiment. Defaults to None.
            params (dict, optional): Variable parameters to be considered for this run. Defaults to None.
            fields (dict, optional): fields to be tracked. Defaults to None.
                only parameter is an instance of the Run class itself.
        """

        self.id_run = next_ulid() if id_run is None else str(id_run)
        self.config = Bunch(config)
        self.params = Bunch(params)
        self.fields = Bunch(fields)
        self.state = Bunch(fields)
        self.vars = Bunch()

        # Execution state and steps to be executed
        self.steps = normalize_steps(steps)
        self.exception = None

    def __getstate__(self):
        state = {key: getattr(self, key) for key in self.__state__}
        return state

    def __setstate__(self, state):
        self.steps = []
        self.vars = Bunch()
        for k, v in state.items():
            self.__setattr__(k, v)

    def __setitem__(self, key, item):
        self.fields[key] = item

    def __getitem__(self, key):
        print(key)
        return self.fields[key]

    def execute_func(self, steps=None, config=None, options=None):
        """Return function that executes a list of steps with config on the run.

        Args:
            steps (_type_, optional): Steps to execute. Defaults to None.
            config (_type_, optional): Fixed arguments. Defaults to None.

        Returns:
            _type_: _description_
        """
        return partial(lambda run: run.execute(steps=steps, config=config, options=options), self)

    def execute(self, steps=None, config=None, options=None):
        """Execute a list of steps with a list of fixed arguments on the run.
            This method might run on different tasks, locally or remotely.

        Args:
            steps (_type_, optional): Steps to execute. Defaults to None.
            config (_type_, optional): Fixed arguments. Defaults to None.

        Returns:
            _type_: _description_
        """

        # Set options to what has been passed by the driver process.
        # This ensures that options changed at runtime are honored in runs execution.
        global_options.copy_from(options.options)

        # Determine random seed for this run, combining the UUID of the run and the
        # value of "reproducibility.random_seed". We initialise both Numpy and Random seeds.
        random_seed = (hash(self.id_run) + global_options.get("reproducibility.random_seed")) % (2**32 - 1)
        np.random.seed(random_seed)
        random.seed(random_seed)

        self.steps = normalize_steps(steps)
        self.config = Bunch(config)
        self.exception = None

        for step in self.steps:
            try:
                step(self)
            except Exception:  # noqa
                self.exception = RunException(exception_message())
                break

        # Clear attributes that should not be accessed after the execution of steps.
        self.steps = None
        self.vars = None

        return self

    def apply(self, func):
        """Apply function to run

        Args:
            func (_type_): Function to apply.
        """
        func(self)

    def _repr_html_(self):
        """Return HTML representation of run, useful in notebooks.

        Returns:
            _type_: _description_
        """
        return f'Run(id="{self.id_run}")'

    def df(self, max_level=0):
        """Represent run as a Pandas dataframe.

        Args:
            max_level (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        # Load the dataframe from a dict or list of dicts.

        df = json_normalize([{**run.fields, **{"id_run": run.id_run}} for run in [self]], max_level=max_level)

        return reorder_columns(df, ["id_run"])


def normalize_steps(steps):
    """Normalize steps, s.t. we always have a list of functions (which might be empty).

    Args:
        steps (_type_): Steps to normalize.

    Returns:
        _type_: _description_
    """
    if steps is None:
        return []
    elif callable(steps):
        return [steps]
    else:
        return steps


def get_params_list(**kwargs):
    """Given a parameter grid, return a list of parameters, with randomised order.

    Returns:
        _type_: _description_
    """
    if not kwargs:
        return [{}]

    params_list = list(Bunch(kwargs).cartesian_product())
    random.Random(global_options.get("reproducibility.random_seed")).shuffle(params_list)
    return params_list
