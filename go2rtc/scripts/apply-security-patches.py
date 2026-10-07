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

\t// Security hardening: configuration mutation, process control and logs are
\t// administrative operations. Never expose them anonymously. If API
\t// credentials are not configured, these endpoints are not registered.
\tif cfg.Mod.Username != "" && cfg.Mod.Password != "" {
\t\tHandleFunc("api/config", adminAuth(cfg.Mod.Username, cfg.Mod.Password, configHandler))
\t\tHandleFunc("api/exit", adminAuth(cfg.Mod.Username, cfg.Mod.Password, exitHandler))
\t\tHandleFunc("api/restart", adminAuth(cfg.Mod.Username, cfg.Mod.Password, restartHandler))
\t\tHandleFunc("api/log", adminAuth(cfg.Mod.Username, cfg.Mod.Password, logHandler))
\t} else {
\t\tlog.Warn().Msg("[api] admin endpoints disabled: set api.username and api.password to enable them")
\t}
''',
)

replace_once(
    api,
    '''func middlewareAuth(username, password string, localAuth bool, next http.Handler) http.Handler {
''',
    '''// adminAuth always requires HTTP Basic authentication, including loopback
// callers. This prevents local_auth=false from bypassing protection for
// sensitive administrative endpoints.
func adminAuth(username, password string, next http.HandlerFunc) http.HandlerFunc {
\thandler := middlewareAuth(username, password, true, next)
\treturn handler.ServeHTTP
}

func middlewareAuth(username, password string, localAuth bool, next http.Handler) http.Handler {
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
