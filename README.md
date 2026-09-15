# NetCheck Lite

A tiny, read-only network health checker for the question every IT admin gets: **“Is the network down, or is it just this service?”**

NetCheck Lite checks DNS resolution, TCP reachability, and TLS certificate validation for endpoints. It uses only Python's standard library and never changes the network, sends credentials, or scans ports.

## Quick start

```bash
python netcheck.py
python netcheck.py --targets sample_targets.json
python netcheck.py --targets sample_targets.json --json
```

Targets are JSON objects with `name`, `host`, and `port`, for example: `[{"name":"Company portal","host":"portal.example.com","port":443}]`.

## Example output

```text
NetCheck Lite — 1/2 checks passed
[PASS] Company portal (example.com:443) — 82.4 ms
[FAIL] Internal DNS example (does-not-exist.invalid:443) — 31.7 ms
       DNS resolution failed
```

Exit code is `0` only when every check passes. Use `--json` for monitoring integrations.

## Why this matters

Fast DNS/TCP/TLS checks separate a local connectivity problem from a service outage before you spend an hour troubleshooting the wrong system.

## Safety

Read-only diagnostic. It checks only the hosts and ports you provide; it does not scan ranges, exploit services, or modify configuration.

Personal project by [BlackPanda999](https://github.com/BlackPanda999).
