# Security policy

This fork exists to harden the Home Assistant go2rtc add-on while preserving Xiaomi, RTSP, WebRTC and FFmpeg functionality.

## Threat model

The primary issue addressed by this fork is AlexxIT/go2rtc issue #2298. In upstream v1.9.14, the HTTP API can expose and modify the raw configuration and can restart/exit the process. Combined with an unrestricted `exec:` source, that can turn LAN API exposure into remote code execution.

## Hardening in 1.9.14-sec.1

- `/api/config`, `/api/restart`, `/api/exit`, and `/api/log` are treated as administrative endpoints.
- Administrative endpoints are not registered unless both `api.username` and `api.password` are configured.
- Administrative endpoints always require HTTP Basic authentication, including loopback clients.
- `exec:` is restricted to `ffmpeg` by default. Additional binaries require an explicit `exec.allow_paths` configuration.

## Recommended go2rtc.yaml

```yaml
api:
  username: go2rtc
  password: CHANGE_THIS_TO_A_LONG_RANDOM_PASSWORD
  local_auth: true

exec:
  allow_paths:
    - ffmpeg
```

Do not expose ports 1984, 8554 or 8555 directly to the public Internet.

## Upstream

Base revision: AlexxIT/go2rtc v1.9.14 commit `b5948cfb25404cc5cb37b166ecaa2dca20b11d4b`.
