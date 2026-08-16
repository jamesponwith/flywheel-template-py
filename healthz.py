"""The Operate stage's half of the contract (ADR 0003).

Keep this when you replace main.py: tools/watch probes it, and the version it
reports is what lets the Learn stage attribute an incident to a release.

Stdlib only, and framework-agnostic — `healthz()` returns the payload, so it
drops into FastAPI, Flask, or a bare http.server without dragging a web
framework into a template that may not need one.
"""

import json
import os
import time

# Set at build/deploy time. The Go template injects this with an ldflag; here
# the deploy sets FLYWHEEL_VERSION, and "dev" means nobody told us.
VERSION = os.environ.get("FLYWHEEL_VERSION", "dev")

_STARTED = time.monotonic()


def healthz(status: str = "ok") -> dict[str, object]:
    """Return the payload tools/watch expects.

    Anything other than status "ok" is a breach. Report "degraded" rather than
    failing outright when the service is up but impaired — watch treats it as a
    breach either way, but the incident then says why.
    """
    return {
        "status": status,
        "version": VERSION,
        "uptime_s": int(time.monotonic() - _STARTED),
    }


def healthz_response(status: str = "ok") -> tuple[int, str, str]:
    """Return (http_status, content_type, body).

    Always HTTP 200, even when degraded: a 5xx here is indistinguishable from
    the process being down, and the body already carries the detail.
    """
    return 200, "application/json", json.dumps(healthz(status))
