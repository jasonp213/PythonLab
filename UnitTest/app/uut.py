from __future__ import annotations

from UnitTest.app.decorators import func_decor


@func_decor
def unit_to_be_tested(*args, **kwargs):
    return args, kwargs
