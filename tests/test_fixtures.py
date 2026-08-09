# ----------------------------------------------------------------------
# Tests against predefined fixtures
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Thor modules
from .utils.fixture import Fixture


def test_api(
    isolated_fixture: Fixture,
    # subtests  # @todo: Uncomment after migration to python 3.10
) -> None:
    for step in isolated_fixture.iter_api_steps():
        # @todo: Starting from python 3.10
        # with subtests.test("api test", step=step.name):
        step.test()
