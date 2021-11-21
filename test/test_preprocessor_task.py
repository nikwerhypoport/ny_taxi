from typing import Set

import pytest

from etl.preprocessor_task import _get_columns_to_drop


@pytest.mark.parametrize(
    "all_columns, columns_to_keep, expected_columns_to_drop",
    [
        ({"a", "b", "c", "d"}, {"b", "c"}, {"a", "d"}),
        ({"a", "d", "j"}, {"b", "c"}, {"a", "d", "j"}),
        ({"b", "c"}, {"b", "c", "not_in_all_columns"}, set()),
    ],
)
def test_get_columns_to_drop(
    all_columns: Set, columns_to_keep: Set, expected_columns_to_drop: Set
):
    assert (
        _get_columns_to_drop(all_columns, columns_to_keep) == expected_columns_to_drop
    )
