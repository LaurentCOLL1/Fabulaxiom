"""Synthetic-only WebView2 ancestry decision model; NOT a Windows observer.

The matching PowerShell candidate is parsed (never executed) on Windows CI.
These fixtures demonstrate fail-closed expected cases, not runtime parity.
"""


class LineageStop(ValueError):
    pass


def classify(processes, get_process_webview_pids, max_depth=12):
    if not isinstance(processes, list) or not isinstance(get_process_webview_pids, list):
        raise LineageStop("invalid process fixture")
    by_pid = {}
    for process in processes:
        pid = process["pid"]
        if not isinstance(pid, int) or pid <= 0 or pid in by_pid:
            raise LineageStop("duplicate/invalid PID")
        by_pid[pid] = process
    if any(p["name"].lower() in ("fabulaxiom.exe", "ollama.exe",
                                 "fabulaxiom", "ollama") for p in processes):
        raise LineageStop("related application")
    edge = [p for p in processes if p["name"].lower() == "msedgewebview2.exe"]
    if sorted(p["pid"] for p in edge) != sorted(get_process_webview_pids):
        raise LineageStop("snapshot mismatch")
    for child in edge:
        node = child
        visited = set()
        for depth in range(max_depth):
            if node["pid"] in visited:
                raise LineageStop("cycle")
            visited.add(node["pid"])
            if node["name"].lower() == "searchhost.exe":
                break
            parent = by_pid.get(node["parent"])
            if parent is None:
                raise LineageStop("missing parent")
            if (node.get("created") is None or parent.get("created") is None or
                    parent["created"] > node["created"]):
                raise LineageStop("invalid timestamps")
            node = parent
        else:
            raise LineageStop("untrusted ancestor")
    return {"metadata_only": True, "searchhost_descendant_count": len(edge),
            "owner_authenticated": False, "sqlite_writer_absent_proven": False}
