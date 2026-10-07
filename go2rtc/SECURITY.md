# Security policy

This fork hardens the Home Assistant go2rtc add-on while preserving Xiaomi, RTSP, WebRTC and FFmpeg functionality.

## Threat model

The primary issue addressed by this fork is AlexxIT/go2rtc issue #2298. In upstream v1.9.14, the HTTP API exposes raw configuration operations and process-control endpoints. Combined with an unrestricted `exec:` source, a client that can reach the API can potentially recover credentials, modify configuration, and escalate a configuration-write primitive into code execution.

## Hardening in 1.9.14-sec.1

- `/api/config` is not registered.
- `/api/restart` is not registered.
- `/api/exit` is not registered.
- `/api/log` is not registered because logs may contain sensitive source details.
- Xiaomi onboarding remains available through `/api/xiaomi`.
- Normal stream APIs, RTSP and WebRTC remain available.
- `exec:` is restricted to `ffmpeg` by default. Additional binaries require an explicit `exec.allow_paths` configuration.
- The upstream source revision is pinned to the exact v1.9.14 commit for reproducible patching.

## Recommended go2rtc.yaml

```yaml
exec:
  allow_paths:
    - ffmpeg
```

You may still configure the normal API username/password if you want an additional authentication layer:

```yaml
api:
  username: go2rtc
  password: CHANGE_THIS_TO_A_LONG_RANDOM_PASSWORD
```

Note that Home Assistant Ingress behavior should be tested before enabling `local_auth: true`.

Do not expose ports 1984, 8554 or 8555 directly to the public Internet.

## Functional trade-off

The generic go2rtc web configuration editor cannot use `/api/config` in this hardened build. Edit `/config/go2rtc.yaml` through Home Assistant/File Editor/SSH instead. Xiaomi Add/Login remains supported because it uses `/api/xiaomi` and `app.PatchConfig()` rather than the raw config endpoint.

## Upstream

Base revision: AlexxIT/go2rtc v1.9.14 commit `b5948cfb25404cc5cb37b166ecaa2dca20b11d4b`.
