from __future__ import annotations

import contextlib
import functools
import hashlib
import inspect
import itertools
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pyarrow as pa
import pyarrow.dataset as ds
from numpy.typing import ArrayLike

from octoflow import config
from octoflow.data.base import PyArrowWrapper
from octoflow.data.compute import Expression

try:
    import pandas as pd
    from pandas import DataFrame as DataFrameType
except ImportError:
    pd = None
    DataFrameType = None


DatasetType = PyArrowWrapper[ds.Dataset]
SourceType = Union[str, List[str], Union[Path, List[Path]], "Dataset", List["Dataset"]]

DEFAULT_BATCH_SIZE = 131_072
DEFAULT_FORMAT = "arrow"


def mapfunc(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        output = func(*args, **kwargs)
        if isinstance(output, pd.Series):
            return output
        return pd.Series(output)

    return wrapped


def get_data_path(path: Union[Path, str]) -> Path:
    if isinstance(path, str):
        path = Path(path)
    if path.is_dir() or not path.exists():
        path.mkdir(
            parents=True,
            exist_ok=True,
        )
        data_path = path / "data"
    else:
        msg = f"expected path to be directory, got '{path}'"
        raise ValueError(msg)
    return data_path


class Dataset(DatasetType):
    def __init__(
        self,
        data: Union[List[dict], Dict[str, list], DataFrameType] = None,
        path: Optional[Union[str, Path]] = None,
        format: str = DEFAULT_FORMAT,
    ):
        # private attributes
        if path is None:
            # create a temporary directory in system temp directory
            cache_dir = Path(config.resources.path).expanduser() / "cache" / "datasets"
            if not cache_dir.exists():
                cache_dir.mkdir(parents=True, exist_ok=True)
            path = Path(tempfile.mkdtemp(dir=cache_dir))
        data_path = get_data_path(path)
        self._path = path
        self._format = format
        ds.write_dataset(pa.table(data), data_path, format=format)
        dataset: ds.Dataset = ds.dataset(data_path, format=self._format)
        super().__init__(dataset)

    @classmethod
    def load_dataset(
        cls,
        path: Union[Path, str],
        format: str = DEFAULT_FORMAT,
    ) -> Dataset:
        # create instance using __new__
        inst = cls.__new__(cls)
        inst._path = path
        inst._format = format
        inst._wrapped = ds.dataset(
            get_data_path(path),
            format=inst._format,
        )
        return inst

    @property
    def path(self) -> Path:
        return self._path

    @property
    def format(self) -> str:
        return self._format

    @property
    def _wrapped_format_default_extname(self) -> str:
        return self._wrapped.format.default_extname

    def count_rows(self) -> int:
        return self._wrapped.count_rows()

    def head(
        self,
        num_rows: int = 5,
        columns: Union[str, List[str], None] = None,
        filter: Expression = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> DataFrameType:
        filter = filter.to_pyarrow() if filter else None
        if isinstance(columns, str):
            columns = [columns]
        table: pa.Table = self._wrapped.head(
            num_rows=num_rows,
            columns=columns,
            filter=filter,
            batch_size=batch_size,
        )
        return table.to_pandas()

    def take(
        self,
        indices: Union[int, slice, List[int], ArrayLike] = [],
        columns: Union[str, List[str], None] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> DataFrameType:
        """
        Take rows from the dataset.

        Parameters
        ----------
        indices : int, slice, list of int, array-like
            Indices of rows to take.
        columns : str, list of str, None
            Names of columns to take. If None, all columns are taken.
        batch_size : int
            Number of rows to take at a time.

        Returns
        -------
        DataFrameType
            A pandas DataFrame containing the taken rows.
        """
        if isinstance(indices, int):
            indices = [indices]
        elif isinstance(indices, slice):
            step_size = indices.step
            if step_size is None:
                # default step size is 1
                step_size = 1
            elif not isinstance(step_size, int):
                msg = f"expected indices.step to be int, got '{indices.step}'"
                raise ValueError(msg)
            elif step_size < 1:
                msg = f"expected indices.step to be greater than 0, got '{step_size}'"
                raise ValueError(msg)
            start = indices.start or 0
            stop = indices.stop or self.count_rows()
            indices = np.arange(start, stop, step_size)
        if isinstance(columns, str):
            columns = [columns]
        table: pa.Table = self._wrapped.take(
            indices=indices,  # array or array-like
            columns=columns,  # list of str or None
            batch_size=batch_size,  # int
        )
        return table.to_pandas()

    def __getitem__(self, indices: Union[int, slice, List[int]]) -> Dataset:
        return self.take(indices)

    def _sync_pyarrow_dataset(
        self,
        suffix: Union[str, Path, None],
        data: Union[
            ds.Dataset,
            pa.RecordBatch,
            pa.Table,
            List[pa.RecordBatch],
            List[pa.Table],
        ],
        schema: pa.Schema = None,
    ) -> Dataset:
        out_path = self.path if suffix is None else self.path / suffix
        if not out_path.exists():
            # first write to temporary directory
            temp_path = Path(tempfile.mkdtemp(dir=self.path / ".tmp"))
            ds.write_dataset(
                data,
                temp_path,
                schema=schema,
                format=self.format,
            )
            out_data_path = get_data_path(out_path)
            with contextlib.suppress(OSError):
                os.replace(temp_path, out_data_path)
        if suffix is None:
            return self
        return type(self).load_dataset(out_path)

    def map(
        self,
        func: Any,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> Dataset:
        batch_iter = (
            pa.RecordBatch.from_pandas(
                batch.to_pandas().apply(
                    mapfunc(func),
                    axis=1,
                ),
            )
            for batch in self._wrapped.to_batches(batch_size=batch_size)
        )
        try:
            first: pa.RecordBatch = next(batch_iter)
        except StopIteration:
            return self
        batch_iter = itertools.chain([first], batch_iter)
        schema = None if first is None else first.schema
        func_hash = hashlib.sha256(inspect.getsource(func).encode()).hexdigest()
        return self._sync_pyarrow_dataset(f"mapped-{func_hash}", batch_iter, schema)

    def filter(self, expression: Expression = None) -> Dataset:
        if expression is None:
            return self
        pyarrow_expression = expression.to_pyarrow()
        dataset = self._wrapped.filter(pyarrow_expression)
        expr_hash = hashlib.sha256(str(pyarrow_expression).encode()).hexdigest()
        return self._sync_pyarrow_dataset(f"filter-{expr_hash}", dataset, dataset.schema)

    def cleanup(self):
        if not self.path.exists():
            return
        shutil.rmtree(self.path)

    def __enter__(self) -> Dataset:
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with contextlib.suppress(Exception):
            self.cleanup()
