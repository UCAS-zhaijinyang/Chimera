# ========= Copyright 2023-2026 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2026 @ CAMEL-AI.org. All Rights Reserved. =========
"""Background Process registry with timeout kill and day-end reaping.

Phase-2 task workers are started asynchronously so the day simulation can
keep advancing. This registry tracks those processes, kills ones that exceed
``task_process_timeout``, and joins/cleans everything at day end so the main
process does not hang after summaries are written.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from multiprocessing import Process
from typing import List, Optional


@dataclass
class _TrackedProcess:
    process: Process
    label: str
    started_at: float


class ProcessRegistry:
    def __init__(self, timeout_seconds: float) -> None:
        self.timeout_seconds = float(timeout_seconds)
        self._lock = threading.Lock()
        self._entries: List[_TrackedProcess] = []

    def register(self, process: Process, label: str = "") -> Process:
        entry = _TrackedProcess(
            process=process,
            label=label or f"pid={getattr(process, 'pid', None)}",
            started_at=time.time(),
        )
        with self._lock:
            self._entries.append(entry)
        return process

    def start(self, process: Process, label: str = "") -> Process:
        process.start()
        return self.register(process, label=label)

    def reap_finished(self) -> None:
        with self._lock:
            alive: List[_TrackedProcess] = []
            for entry in self._entries:
                if entry.process.is_alive():
                    alive.append(entry)
                else:
                    entry.process.join(timeout=0)
            self._entries = alive

    def kill_timed_out(self) -> int:
        """Terminate processes that exceeded the timeout. Returns kill count."""
        now = time.time()
        killed = 0
        with self._lock:
            still_tracked: List[_TrackedProcess] = []
            for entry in self._entries:
                if not entry.process.is_alive():
                    entry.process.join(timeout=0)
                    continue
                age = now - entry.started_at
                if age >= self.timeout_seconds:
                    print(
                        f"[WARN] Killing timed-out task process "
                        f"{entry.label} (pid={entry.process.pid}, "
                        f"age={age:.0f}s > {self.timeout_seconds:.0f}s)."
                    )
                    self._force_kill(entry.process)
                    killed += 1
                else:
                    still_tracked.append(entry)
            self._entries = still_tracked
        return killed

    def reap_all(self, final_join_timeout: float = 10.0) -> None:
        """Kill remaining live processes and join everything."""
        with self._lock:
            entries = list(self._entries)
            self._entries = []

        for entry in entries:
            if entry.process.is_alive():
                print(
                    f"[WARN] Reaping unfinished task process "
                    f"{entry.label} (pid={entry.process.pid})."
                )
                self._force_kill(entry.process)
            entry.process.join(timeout=final_join_timeout)

    def poll(self) -> None:
        """Drop finished workers and kill any that exceeded timeout."""
        self.reap_finished()
        self.kill_timed_out()

    @staticmethod
    def _force_kill(process: Process) -> None:
        if not process.is_alive():
            process.join(timeout=0)
            return
        process.terminate()
        process.join(timeout=5)
        if process.is_alive():
            process.kill()
            process.join(timeout=5)


# Module-level registry used by Phase-2 / attack day runners.
_REGISTRY: Optional[ProcessRegistry] = None
_REGISTRY_LOCK = threading.Lock()


def init_registry(timeout_seconds: float) -> ProcessRegistry:
    global _REGISTRY
    with _REGISTRY_LOCK:
        _REGISTRY = ProcessRegistry(timeout_seconds=timeout_seconds)
        return _REGISTRY


def get_registry() -> Optional[ProcessRegistry]:
    return _REGISTRY


def start_tracked(process: Process, label: str = "") -> Process:
    registry = get_registry()
    if registry is None:
        process.start()
        return process
    return registry.start(process, label=label)


def poll_registry() -> None:
    registry = get_registry()
    if registry is not None:
        registry.poll()


def reap_all_tracked(final_join_timeout: float = 10.0) -> None:
    registry = get_registry()
    if registry is not None:
        registry.reap_all(final_join_timeout=final_join_timeout)
