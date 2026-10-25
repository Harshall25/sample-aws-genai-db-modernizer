"""Expression index keys, as the collectors report them (#295).

``pg_index.indkey`` holds 0 for an expression key, and 0 is never an
``attnum``, so an expression key never comes back as a column name. The
queries report it as a flag plus the expression text instead. This is the one
place that reads those raw columns, so the live path and the offline path put
the same thing on the contract.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

# Both a JSON dump and a psql text dump reach us, so the boolean arrives
# either already parsed or as PostgreSQL's own 't'/'f'.
_TRUTHY = (True, 1, "t", "true", "1")


def expression_key_fields(row: Mapping[str, Any]) -> dict[str, Any]:
    """The ``Index`` fields describing one raw index row's expression keys.

    The two text fields ride along only for an index that actually has
    expression keys: ``pg_get_indexdef`` is never null, and carrying every
    plain index's CREATE statement into every schema designer's prompt would
    be a lot of text that says nothing the columns don't already.
    """
    if row.get("has_expressions") not in _TRUTHY:
        return {"has_expressions": False, "index_expressions": None, "index_def": None}
    return {
        "has_expressions": True,
        "index_expressions": row.get("index_expressions") or None,
        "index_def": row.get("index_def") or None,
    }
