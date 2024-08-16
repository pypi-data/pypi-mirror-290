# airflow-serde-polars

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-yellow.svg)](https://opensource.org/licenses/Apache-2.0)
[![github action](https://github.com/phi-friday/airflow-serde-polars/actions/workflows/check.yaml/badge.svg?event=push)](#)
[![PyPI version](https://badge.fury.io/py/airflow-serde-polars.svg)](https://badge.fury.io/py/airflow-serde-polars)
[![python version](https://img.shields.io/pypi/pyversions/airflow-serde-polars.svg)](#)

## how to install
```sh
pip install airflow-serde-polars
```

## how to use

You don't need to call it specifically after installation.
Serialization is done automatically when passing frames to XCOM.

### example dag
```python
from __future__ import annotations

from typing import TYPE_CHECKING

from pendulum import datetime

from airflow.decorators import dag, task

if TYPE_CHECKING:
    import polars as pl


@dag(start_date=datetime(2024, 1, 1), schedule=None, catchup=False)
def polars_sample():
    @task.python(do_xcom_push=True)
    def return_polars_frame() -> pl.DataFrame:
        import polars as pl

        return pl.DataFrame(
            {
                "a": [1, 2, 3],
                "b": [4, 5, 6],
            }
        )

    @task.python(do_xcom_push=False)
    def print_polars_frame(df: pl.DataFrame) -> None:
        from pprint import pprint

        pprint(df)

    frame = return_polars_frame()
    show = print_polars_frame(frame)  # pyright: ignore[reportArgumentType]

    _ = frame >> show


polars_sample()
```

## Is this an airflow provider?
It's created for a similar purpose, but it's not a provider.
The airflow providers meta information does not define a serializer.

When I am able to enter the provider meta information as a serializer,
I will update the library to match the provider conditions.