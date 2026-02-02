import time
from collections import defaultdict
from threading import Lock
from collections import Counter

class MetricsStore:
    def __init__(self):
        self.lock = Lock()
        self.request_count = 0
        self.error_count = 0
        self.latencies = []

    def record(self, latency_ms: float, is_error: bool):
        with self.lock:
            self.request_count += 1
            if is_error:
                self.error_count += 1
            self.latencies.append(latency_ms)

    def snapshot(self):
        with self.lock:
            latencies = sorted(self.latencies)
            count = len(latencies)

            def percentile(p):
                if count == 0:
                    return 0.0
                idx = int(count * p)
                idx = min(idx, count - 1)
                return latencies[idx]

            return {
                "requests_total": self.request_count,
                "errors_total": self.error_count,
                "p50_latency_ms": percentile(0.50),
                "p95_latency_ms": percentile(0.95),
            }

class RetrievalMetrics:
    def __init__(self):
        self.decisions = Counter()

    def record(self, decision: str):
        self.decisions[decision] += 1

    def snapshot(self):
        return dict(self.decisions)
