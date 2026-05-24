#!/usr/bin/env python3
"""Bridge incoming Signal messages from signal-cli JSON-RPC to pi RPC."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import re
import shlex
import socket
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Any


class JsonLineSocket:
    def __init__(self, host: str, port: int):
        self.sock = socket.create_connection((host, port), timeout=15)
        # Use a timeout only for the initial connect. Once connected, the
        # bridge must be able to sit idle indefinitely waiting for Signal
        # receive notifications without raising TimeoutError.
        self.sock.settimeout(None)
        self.file = self.sock.makefile("r", encoding="utf-8", newline="\n")
        self.lock = threading.Lock()

    def send(self, obj: dict[str, Any]) -> None:
        data = json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n"
        with self.lock:
            self.sock.sendall(data.encode("utf-8"))

    def lines(self):
        while True:
            line = self.file.readline()
            if not line:
                raise EOFError("signal-cli JSON-RPC socket closed")
            yield json.loads(line)


def safe_tmux_name(prefix: str, key: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", key).strip("-")[:45] or "thread"
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{slug}-{digest}"[:90]


class PiRpc:
    def __init__(self, command: list[str], cwd: str, tmux_session: str | None = None, runtime_dir: Path | None = None):
        self.lock = threading.Lock()
        self.tmux_session = tmux_session
        if tmux_session:
            self.proc = None
            self.stdin, self.stdout = self._start_tmux_rpc(command, cwd, tmux_session, runtime_dir)
        else:
            self.proc = subprocess.Popen(
                command,
                cwd=cwd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
            assert self.proc.stdin and self.proc.stdout
            self.stdout = self.proc.stdout
            self.stdin = self.proc.stdin
            threading.Thread(target=self._log_stderr, daemon=True).start()

    def _start_tmux_rpc(self, command: list[str], cwd: str, session: str, runtime_dir: Path | None):
        base = runtime_dir or Path("/tmp/pi-signal-subagents")
        run_dir = base / session
        run_dir.mkdir(parents=True, exist_ok=True)
        stdin_fifo = run_dir / "stdin.fifo"
        stdout_fifo = run_dir / "stdout.fifo"
        stderr_log = run_dir / "stderr.log"
        for fifo in (stdin_fifo, stdout_fifo):
            if fifo.exists():
                fifo.unlink()
            os.mkfifo(fifo, 0o600)
        subprocess.run(["tmux", "kill-session", "-t", session], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cmd = " ".join(shlex.quote(part) for part in command)
        script = f"exec {cmd} < {shlex.quote(str(stdin_fifo))} > {shlex.quote(str(stdout_fifo))} 2>> {shlex.quote(str(stderr_log))}"
        subprocess.run(["tmux", "new-session", "-d", "-s", session, "-c", cwd, "bash", "-lc", script], check=True)
        # Open stdin first. The tmux-side shell opens stdin.fifo for reading
        # before it opens stdout.fifo for writing. Opening stdout first here
        # deadlocks both sides and leaves the Signal chat stuck forever.
        stdin = open(stdin_fifo, "w", encoding="utf-8", newline="\n", buffering=1)
        stdout = open(stdout_fifo, "r", encoding="utf-8", newline="\n", buffering=1)
        print(f"[pi subagent] tmux session={session} cwd={cwd} stderr={stderr_log}", file=sys.stderr, flush=True)
        return stdin, stdout

    def _log_stderr(self) -> None:
        assert self.proc and self.proc.stderr
        for line in self.proc.stderr:
            print(f"[pi stderr] {line.rstrip()}", file=sys.stderr, flush=True)

    def prompt(self, message: str) -> str:
        with self.lock:
            req_id = str(uuid.uuid4())
            self.stdin.write(json.dumps({"id": req_id, "type": "prompt", "message": message}, ensure_ascii=False) + "\n")
            self.stdin.flush()
            chunks: list[str] = []
            accepted = False
            for line in self.stdout:
                event = json.loads(line)
                if event.get("type") == "response" and event.get("id") == req_id:
                    if not event.get("success"):
                        raise RuntimeError(event.get("error", "pi rejected prompt"))
                    accepted = True
                    continue
                if event.get("type") == "message_update":
                    delta = event.get("assistantMessageEvent", {})
                    if delta.get("type") == "text_delta":
                        chunks.append(delta.get("delta", ""))
                elif event.get("type") == "agent_end" and accepted:
                    return "".join(chunks).strip() or "(pi completed without a text response)"
            raise EOFError("pi RPC process exited")


def extract_message(notification: dict[str, Any]) -> dict[str, Any] | None:
    if notification.get("method") != "receive":
        return None
    params = notification.get("params") or {}
    envelope = params.get("envelope") or params
    data = envelope.get("dataMessage") or envelope.get("syncMessage", {}).get("sentMessage", {}).get("dataMessage")
    if not data:
        return None
    text = data.get("message") or ""
    if not text.strip():
        return None
    source = envelope.get("sourceNumber") or envelope.get("source") or envelope.get("sourceUuid")
    group = data.get("groupInfo") or data.get("groupV2") or {}
    group_id = group.get("groupId") or group.get("id")
    timestamp = envelope.get("timestamp") or data.get("timestamp")
    return {"text": text, "source": source, "group_id": group_id, "timestamp": timestamp}


def signal_destination_params(dest: dict[str, Any]) -> dict[str, Any]:
    if dest.get("group_id"):
        return {"groupId": dest["group_id"]}
    return {"recipient": [dest["source"]]}


def send_signal(rpc: JsonLineSocket, dest: dict[str, Any], message: str) -> None:
    params: dict[str, Any] = {"message": message, **signal_destination_params(dest)}
    rpc.send({"jsonrpc": "2.0", "method": "send", "params": params, "id": str(uuid.uuid4())})


def send_typing(rpc: JsonLineSocket, dest: dict[str, Any], stop: bool = False) -> None:
    params: dict[str, Any] = signal_destination_params(dest)
    if stop:
        params["stop"] = True
    rpc.send({"jsonrpc": "2.0", "method": "sendTyping", "params": params, "id": str(uuid.uuid4())})


def start_typing_loop(rpc: JsonLineSocket, dest: dict[str, Any], interval: float = 5.0) -> threading.Event:
    done = threading.Event()

    def run() -> None:
        while not done.is_set():
            try:
                send_typing(rpc, dest)
            except Exception as exc:
                print(f"[typing error] {exc}", file=sys.stderr, flush=True)
            done.wait(interval)

    threading.Thread(target=run, daemon=True).start()
    return done


def chunks(text: str, size: int):
    start = 0
    while start < len(text):
        yield text[start : start + size]
        start += size


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="/root/.pi/agent/signal-bridge/config.json")
    args = ap.parse_args()
    cfg = json.loads(Path(args.config).read_text())

    signal_cfg = cfg["signal"]
    bridge_cfg = cfg.get("bridge", {})
    pi_cfg = cfg["pi"]
    allowed = set(signal_cfg.get("allowed_senders") or [])
    allow_groups = bool(signal_cfg.get("allow_groups", False))
    dm_trigger_prefix = bridge_cfg.get("dm_trigger_prefix", bridge_cfg.get("trigger_prefix", ""))
    group_trigger_prefix = bridge_cfg.get("group_trigger_prefix", bridge_cfg.get("trigger_prefix", ""))
    max_chars = int(bridge_cfg.get("max_signal_message_chars", 3500))
    prefix = pi_cfg.get("system_prefix", "")

    signal_rpc = JsonLineSocket(signal_cfg["host"], int(signal_cfg["port"]))
    use_subagents = bool(bridge_cfg.get("tmux_subagents", True))
    subagent_backend = bridge_cfg.get("subagent_backend", "process")
    use_tmux = use_subagents and subagent_backend == "tmux"
    worker_count = int(bridge_cfg.get("worker_count", 8 if use_subagents else 1))
    runtime_dir = Path(bridge_cfg.get("runtime_dir", "/tmp/pi-signal-subagents"))
    default_pi = None if use_subagents else PiRpc(pi_cfg["command"], pi_cfg.get("working_directory") or os.getcwd())
    agents: dict[str, PiRpc] = {}
    agents_lock = threading.Lock()
    work: queue.Queue[dict[str, Any]] = queue.Queue()

    def thread_key(item: dict[str, Any]) -> str:
        if item.get("group_id"):
            return f"group:{item['group_id']}"
        return f"dm:{item.get('source') or 'unknown'}"

    def agent_for(item: dict[str, Any]) -> PiRpc:
        if not use_subagents:
            assert default_pi is not None
            return default_pi
        key = thread_key(item)
        with agents_lock:
            agent = agents.get(key)
            if agent is None:
                session = safe_tmux_name("pi-signal", key)
                if use_tmux:
                    agent = PiRpc(pi_cfg["command"], pi_cfg.get("working_directory") or os.getcwd(), session, runtime_dir)
                else:
                    agent = PiRpc(pi_cfg["command"], pi_cfg.get("working_directory") or os.getcwd())
                    print(f"[pi subagent] process key={key} session={session}", file=sys.stderr, flush=True)
                agents[key] = agent
            return agent

    def worker() -> None:
        while True:
            item = work.get()
            try:
                user_text = item["text"]
                route_prefix = item.get("matched_prefix", "")
                if route_prefix:
                    user_text = user_text[len(route_prefix) :].lstrip()
                prompt = f"{prefix}\n\nSignal message from {item.get('source') or 'unknown'}:\n{user_text}" if prefix else user_text
                typing_done = start_typing_loop(signal_rpc, item) if bridge_cfg.get("send_typing", True) else None
                try:
                    reply = agent_for(item).prompt(prompt)
                finally:
                    if typing_done:
                        typing_done.set()
                        send_typing(signal_rpc, item, stop=True)
                for part in chunks(reply, max_chars):
                    send_signal(signal_rpc, item, part)
            except Exception as exc:
                if use_subagents:
                    with agents_lock:
                        agents.pop(thread_key(item), None)
                try:
                    send_signal(signal_rpc, item, f"pi bridge error: {exc}")
                except Exception:
                    pass
                print(f"[bridge error] {exc}", file=sys.stderr, flush=True)
            finally:
                work.task_done()

    for _ in range(max(1, worker_count)):
        threading.Thread(target=worker, daemon=True).start()
    print("Signal ↔ pi bridge is running", flush=True)

    for event in signal_rpc.lines():
        msg = extract_message(event)
        if not msg:
            continue
        if msg.get("group_id") and not allow_groups:
            continue
        if allowed and msg.get("source") not in allowed:
            continue
        route_prefix = group_trigger_prefix if msg.get("group_id") else dm_trigger_prefix
        if route_prefix and not msg["text"].startswith(route_prefix):
            continue
        msg["matched_prefix"] = route_prefix
        work.put(msg)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
