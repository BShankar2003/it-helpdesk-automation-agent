# observability/tracing.py
import time, json, os

def start_trace_span(name, attrs=None):
    start = time.time()
    trace = {
        "name": name,
        "start": start,
        "attrs": attrs or {}
    }

    class Span:
        def set_attribute(self, key, value):
            trace["attrs"][key] = value

        def end(self):
            trace["end"] = time.time()
            trace["duration_ms"] = round((trace["end"] - trace["start"]) * 1000, 2)

            os.makedirs("observability/traces", exist_ok=True)
            file = f"observability/traces/{int(start*1000)}_{name}.json"
            with open(file, "w") as f:
                json.dump(trace, f, indent=2)

    return Span()
