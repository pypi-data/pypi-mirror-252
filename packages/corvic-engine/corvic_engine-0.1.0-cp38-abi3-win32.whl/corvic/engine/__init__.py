"""Engine bindings."""

# Allow linting to proceed without extension module. _native.pyi should be
# authoritative anyway.
from corvic.engine._native import (  # pyright: ignore[reportMissingModuleSource]
    sum_as_string,
)

# Manually expose and type native symbols. pyo3 does not generate typing
# information that Python type checkers understand [1] and extension modules
# cannot be marked as typed directly [2]. The sensible resolution is to expose
# extension modules through a typed wrapper.
#
# [1] https://github.com/PyO3/pyo3/issues/2454
# [2] https://github.com/python/typing/issues/1333.


__all__ = [
    "sum_as_string",
]
