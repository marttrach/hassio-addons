#!/usr/bin/env python3
from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one patch target, found {count}")
    path.write_text(text.replace(old, new, 1))


api = Path("internal/api/api.go")

replace_once(
    api,
    '''\tHandleFunc("api", apiHandler)
\tHandleFunc("api/config", configHandler)
\tHandleFunc("api/exit", exitHandler)
\tHandleFunc("api/restart", restartHandler)
\tHandleFunc("api/log", logHandler)
''',
    '''\tHandleFunc("api", apiHandler)

\t// Security hardening: do not expose raw configuration, process control,
\t// or in-memory logs over HTTP. Xiaomi onboarding uses /api/xiaomi and
\t// normal stream management uses their own validated endpoints, so these
\t// high-risk administrative endpoints are intentionally disabled.
\tlog.Info().Msg("[api] security hardening enabled: config/restart/exit/log HTTP endpoints disabled")
''',
)

exec_go = Path("internal/exec/exec.go")

replace_once(
    exec_go,
    '''\tallowPaths = cfg.Mod.AllowPaths
''',
    '''\tallowPaths = cfg.Mod.AllowPaths
\tif allowPaths == nil {
\t\t// Secure-by-default: arbitrary exec sources turn a config-write bug into
\t\t// code execution. ffmpeg is the only executable allowed unless the user
\t\t// explicitly opts in to additional binaries.
\t\tallowPaths = []string{"ffmpeg"}
\t}
''',
)

print("Applied go2rtc security hardening patches")
