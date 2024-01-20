"""Code generated by __main__"""

from dataclasses import dataclass, field
from typing import List

from sigtech.api.data.utils import BaseRule


@dataclass
class LargeGapsRule(BaseRule):
    """
    For the selected columns, raise an issue where the gap between the time stamps of two consecutive data points is too long.

    :param columns (List[str]): Select at least one column:
        - minItems: 1
        - uniqueItems: True
    :param gap_size (int): Raise an issue for gaps of:
        - min: 0

    docs: https://sigtech.gitbook.io/dave/rules#gaps
    """  # noqa: E501

    columns: List[str] = field(
        metadata={
            "description": "Select at least one column:",
            "minItems": 1,
            "uniqueItems": True,
            "type": "List[str]",
        }
    )

    gap_size: int = field(
        metadata={"description": "Raise an issue for gaps of:", "min": 0, "type": "int"}
    )
