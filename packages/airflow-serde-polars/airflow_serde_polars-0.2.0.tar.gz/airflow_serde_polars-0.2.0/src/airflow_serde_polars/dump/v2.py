from __future__ import annotations

from typing import TYPE_CHECKING, cast

from airflow_serde_polars.utils.parse import find_version

if TYPE_CHECKING:
    from airflow.serialization.serde import U

_version = find_version(__file__)


def serialize(o: object) -> tuple[U, str, int, bool]:  # pyright: ignore[reportUnknownParameterType]
    import polars as pl
    import pyarrow as pa
    from airflow.utils.module_loading import qualname

    from airflow_serde_polars.dump.v1 import serialize as v1_serialize

    if not isinstance(o, pa.Table):
        result = v1_serialize(o)
        if not result[3]:
            return result
        return ((result[0], ""), result[1], _version, True)

    name = qualname(o)
    schema: pa.Schema = o.schema  # pyright: ignore[reportAttributeAccessIssue]

    o = cast("pl.DataFrame", pl.from_arrow(o))
    result = v1_serialize(o)

    if not result[3]:
        return result

    buffer: pa.Buffer = schema.serialize()
    schema_as_bytes: bytes = buffer.to_pybytes()
    schema_as_hex = schema_as_bytes.hex()

    return ((result[0], schema_as_hex), name, _version, True)
