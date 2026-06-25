#!/usr/bin/env python3
"""Create a detached tmux session on an EC2/bastion host over SSH.

Intended to be run through with_aws_access.py --ssh-key-file so the SSH key is
materialized temporarily and never stored in this repository.
"""
from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone

SESSION_RE = re.compile(r"[^A-Za-z0-9_.:-]+")


def default_session() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"pi-ec2-{stamp}"


def safe_session(value: str) -> str:
    cleaned = SESSION_RE.sub("-", value.strip())[:80].strip("-.")
    if not cleaned:
        raise SystemExit("tmux session name is empty after sanitization")
    return cleaned


def ssh_target(args: argparse.Namespace) -> str:
    host = args.host or os.environ.get("AWS_ACCESS_HOSTNAME")
    user = args.user or os.environ.get("AWS_ACCESS_USERNAME")
    if not host:
        raise SystemExit("Missing host. Pass --host or set AWS_ACCESS_HOSTNAME via with_aws_access.py")
    return f"{user}@{host}" if user else host


def build_remote_script(args: argparse.Namespace) -> str:
    session = safe_session(args.session or default_session())
    command = args.command or "bash -l"
    cwd_prefix = f"cd {shlex.quote(args.cwd)} && " if args.cwd else ""
    log_path = args.log_path or f"~/pi-tmux-{session}.log"
    remote_command = f"{cwd_prefix}{command}"

    if args.replace:
        prelude = f"tmux kill-session -t {shlex.quote(session)} 2>/dev/null || true; "
    else:
        prelude = (
            f"if tmux has-session -t {shlex.quote(session)} 2>/dev/null; then "
            f"echo 'tmux session already exists: {session}' >&2; exit 2; fi; "
        )

    return (
        "set -euo pipefail; "
        "command -v tmux >/dev/null || { echo 'tmux is not installed on remote host' >&2; exit 127; }; "
        f"{prelude}"
        f"tmux new-session -d -s {shlex.quote(session)} "
        f"'bash -lc {shlex.quote(remote_command + ' 2>&1 | tee -a ' + log_path)}'; "
        f"echo 'started tmux session: {session}'; "
        f"echo 'attach: tmux attach -t {session}'; "
        f"echo 'log: {log_path}'"
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Start a detached tmux session on an EC2 host over SSH")
    parser.add_argument("--host", help="EC2/bastion hostname. Defaults to AWS_ACCESS_HOSTNAME")
    parser.add_argument("--user", help="SSH username. Defaults to AWS_ACCESS_USERNAME")
    parser.add_argument("--key-file", default=os.environ.get("AWS_ACCESS_KEY_FILE"), help="SSH private key path")
    parser.add_argument("--session", help="Remote tmux session name. Defaults to pi-ec2-<timestamp>")
    parser.add_argument("--command", default="bash -l", help="Command to run inside the remote tmux session")
    parser.add_argument("--cwd", help="Remote working directory before running command")
    parser.add_argument("--log-path", help="Remote log path. Defaults to ~/pi-tmux-<session>.log")
    parser.add_argument("--replace", action="store_true", help="Kill an existing remote tmux session with the same name first")
    parser.add_argument("--ssh-option", action="append", default=[], help="Extra ssh -o option, repeatable")
    args = parser.parse_args(argv)

    if not args.key_file:
        raise SystemExit("Missing SSH key file. Run via with_aws_access.py --ssh-key-file or pass --key-file")

    ssh_cmd = [
        "ssh",
        "-i",
        args.key_file,
        "-o",
        "IdentitiesOnly=yes",
        "-o",
        "StrictHostKeyChecking=accept-new",
    ]
    for option in args.ssh_option:
        ssh_cmd.extend(["-o", option])
    ssh_cmd.extend([ssh_target(args), build_remote_script(args)])

    proc = subprocess.run(ssh_cmd)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
