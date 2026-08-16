"""The Operate contract, asserted from the prober's point of view."""

import json

import pytest

import healthz as h


@pytest.mark.parametrize("status", ["ok", "degraded"])
def test_healthz_payload(status: str) -> None:
    got = h.healthz(status)
    assert got["status"] == status
    # Learn attributes an incident to a release through this field.
    assert got["version"] == h.VERSION
    assert isinstance(got["uptime_s"], int) and got["uptime_s"] >= 0


def test_degraded_is_still_200() -> None:
    code, ctype, body = h.healthz_response("degraded")
    # A 5xx is indistinguishable from the process being down; the body carries
    # the detail instead.
    assert code == 200
    assert ctype == "application/json"
    assert json.loads(body)["status"] == "degraded"


def test_body_is_valid_json() -> None:
    # tools/watch treats an unparseable body as a breach.
    _, _, body = h.healthz_response()
    assert json.loads(body)["status"] == "ok"
