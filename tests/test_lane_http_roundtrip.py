import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from evo.interop.lane_http import submit_http_job, wait_http_done


def _server(host: str, port: int):
    state = {"run_id": "csc-xyz", "status": "running", "idem": {}}

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path == "/runs":
                idem = self.headers.get("Idempotency-Key", "")
                if idem in state["idem"]:
                    resp = {"run_id": state["idem"][idem], "accepted": True}
                else:
                    state["idem"][idem] = state["run_id"]
                    resp = {"run_id": state["run_id"], "accepted": True}
                self.send_response(202)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp).encode("utf-8"))
            else:
                self.send_error(404)

        def do_GET(self):
            if self.path == f"/runs/{state['run_id']}":
                body = {"run_id": state["run_id"], "status": state["status"]}
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(body).encode("utf-8"))
            else:
                self.send_error(404)

        def log_message(self, *_args):
            return

    httpd = HTTPServer((host, port), H)
    return httpd, state


def test_http_lane_roundtrip(tmp_path: Path):
    httpd, state = _server("127.0.0.1", 18080)

    def _run():
        # flip to ok after a short delay
        time.sleep(0.2)
        state["status"] = "ok"
        time.sleep(0.1)
        httpd.shutdown()

    t = threading.Thread(target=_run, daemon=True)
    s = threading.Thread(target=httpd.serve_forever, daemon=True)
    s.start()
    t.start()

    cfg = {"http_base": "http://127.0.0.1:18080", "poll_interval_ms": 50}
    bundle = tmp_path / "g010.zip"
    bundle.write_bytes(b"dummy")

    run_id = submit_http_job(cfg, bundle, "g010", 123, {"strict": False})
    rec = wait_http_done(cfg, run_id, timeout_s=5)
    assert rec["status"] == "ok"
