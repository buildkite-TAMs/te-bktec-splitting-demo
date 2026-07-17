import os
import pytest

# Quarantine demo (Lab 4 §4.5). OFF by default so the splitting lab stays green.
# Turn on with RUN_FLAKY_LAB=true to simulate a flaky test that is currently
# FAILING. Un-muted, it fails the build. Once you quarantine (mute) it in the
# suite, bktec soft-fails it and the build goes green again — that's the payoff.


def test_flaky_quarantine_demo():
    if os.environ.get("RUN_FLAKY_LAB") != "true":
        pytest.skip("quarantine demo disabled (set RUN_FLAKY_LAB=true)")
    assert False, "simulated flaky failure — mute me and bktec keeps the build green"
