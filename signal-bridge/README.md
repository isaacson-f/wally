# Signal ↔ pi bridge

This bridge connects the existing `signal-cli` JSON-RPC daemon on `127.0.0.1:7583` to pi RPC mode.

## Files

- `config.json` - bridge settings
- `signal_pi_bridge.py` - bridge process
- `/root/.config/systemd/user/signal-pi-bridge.service` - optional user service

## Configure access

Edit `config.json` before running if you want to restrict who can talk to pi:

```json
"allowed_senders": ["+15551234567"]
```

Leaving `allowed_senders` empty allows any direct sender. Groups are enabled when `allow_groups` is `true`.

Current prefix behavior:

- Direct messages: no prefix required (`dm_trigger_prefix` is `""`)
- Groups: messages must start with `wally` (`group_trigger_prefix` is `"wally"`)

While pi is working, the bridge sends Signal typing indicators instead of a "pi is thinking" message. Set `send_typing` to `false` to disable typing indicators.

Subagents are enabled with `tmux_subagents: true`, but the default `subagent_backend` is `"process"`. This creates one long-lived pi RPC process per DM/group without tmux FIFO plumbing. Set `subagent_backend` to `"tmux"` only if you specifically need tmux-backed sessions.

## Run manually

```bash
python3 /root/.pi/agent/signal-bridge/signal_pi_bridge.py
```

## Run with systemd user service

```bash
systemctl --user daemon-reload
systemctl --user enable --now signal-pi-bridge.service
systemctl --user status signal-pi-bridge.service
journalctl --user -u signal-pi-bridge.service -f
```

The bridge expects `signal-cli daemon --tcp 127.0.0.1:7583` to already be running and pi to already be logged in.
