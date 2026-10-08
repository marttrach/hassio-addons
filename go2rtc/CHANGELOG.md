# 1.9.14-sec.1

Security hardening based on AlexxIT/go2rtc v1.9.14.

- Protect administrative API endpoints behind mandatory Basic Auth.
- Disable administrative endpoints entirely until api.username and api.password are configured.
- Restrict exec sources to ffmpeg by default.
- Pin upstream source commit for reproducible builds.
- Add CI that reapplies the patch, runs Go tests, and builds an amd64 binary.
