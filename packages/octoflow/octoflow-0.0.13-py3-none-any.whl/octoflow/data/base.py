from typing import Generic, TypeVar

ArrowType = TypeVar("ArrowType")


class PyArrowWrapper(Generic[ArrowType]):
    def __init__(self, wrapped: ArrowType) -> None:
        self._wrapped = wrapped

    def to_pyarrow(self) -> ArrowType:
        return self._wrapped
