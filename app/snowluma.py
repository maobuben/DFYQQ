"""SnowLuma 协议端的小工具：下载/校验/解压、写配置、找桌面 QQ、判断连接状态。

SnowLuma 和 NapCat 不一样：它自己不带 QQ，而是挂在本机已经打开、已经登录的桌面 QQ 上，
对外提供和 NapCat 一样的 OneBot v11 接口。AstrBot 那一侧不用改。

SnowLuma 的发行包授权只允许个人使用，不允许二次打包转发，所以这个一键包不内置它：
安装时从官方发布地址下载；下载不到时，也可以由用户把官方 zip 放到安装目录，再点重试。
"""
import ctypes
import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.request
import zipfile
from ctypes import wintypes
from pathlib import Path

from fileio import atomic_write_text

VERSION = "v2.4.2"
SHA256 = "0912926c5e73260f35b000278a8658493fc9452f36782c32fa86f0e825bad81a"
ASSET = f"SnowLuma-{VERSION}-win-x64.zip"
# 官方地址优先；官方仓库偶尔不可用时，用同一个 release 的镜像。都下不动时再让用户手动放 zip。
OFFICIAL = f"https://github.com/SnowLuma/SnowLuma/releases/download/{VERSION}/{ASSET}"
MIRROR = f"https://github.com/TomyJan/SnowLuma/releases/download/{VERSION}/{ASSET}"
URLS = [
    OFFICIAL,
    MIRROR,
    f"https://gh.dpik.top/{OFFICIAL}",
    f"https://gh.dpik.top/{MIRROR}",
    f"https://ghproxy.net/{OFFICIAL}",
    f"https://gh-proxy.com/{MIRROR}",
]
# 用户把官方包放在这些位置都能认：安装目录、安装目录\downloads、解压出来的临时目录。
ZIP_DIRS = ("", "downloads")

DEFAULT_ONEBOT = {
    "networks": {"httpServers": [], "httpClients": [], "wsServers": [], "wsClients": []},
    "musicSignUrl": "",
}


class SnowLumaError(RuntimeError):
    """预期内的失败，message 直接给用户看。"""


def base_dir(root: Path) -> Path:
    return Path(root) / "snowluma"


def config_dir(root: Path) -> Path:
    return base_dir(root) / "config"


def installed(root: Path) -> bool:
    root = Path(root)
    return (base_dir(root) / "node.exe").is_file() and (base_dir(root) / "index.mjs").is_file()


def _read(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2), backup=True)


def write_global_config(root: Path) -> None:
    """全局 onebot.json 什么都不连；每个号单独一份 onebot_<号>.json。"""
    path = config_dir(root) / "onebot.json"
    conf = _read(path) or json.loads(json.dumps(DEFAULT_ONEBOT))
    networks = conf.setdefault("networks", {})
    for key in ("httpServers", "httpClients", "wsServers", "wsClients"):
        networks[key] = []
    conf.setdefault("musicSignUrl", "")
    _write(path, conf)


def write_runtime_config(root: Path, webui_port: int) -> None:
    """网页后台只开在本机，自动挂到已经打开的 QQ 上。"""
    path = config_dir(root) / "runtime.json"
    conf = _read(path)
    conf.update({"webuiPort": int(webui_port), "webuiHost": "127.0.0.1", "hookAutoLoad": True})
    _write(path, conf)


def account_path(root: Path, qq: str) -> Path:
    return config_dir(root) / f"onebot_{qq}.json"


def write_account_config(root: Path, qq: str, onebot_port: int, token: str) -> None:
    """把小号这份配置改成只连本机 AstrBot 的反向 WebSocket。"""
    path = account_path(root, qq)
    conf = _read(path) or json.loads(json.dumps(DEFAULT_ONEBOT))
    networks = conf.setdefault("networks", {})
    for key in ("httpServers", "httpClients", "wsServers"):
        networks[key] = networks.get(key) if isinstance(networks.get(key), list) else []
    networks["wsClients"] = [{
        "name": "astrbot", "enabled": True, "url": f"ws://127.0.0.1:{onebot_port}/ws",
        "role": "Universal", "accessToken": token, "messageFormat": "array",
        "reportSelfMessage": False, "reconnectIntervalMs": 5000,
    }]
    conf.setdefault("musicSignUrl", "")
    _write(path, conf)


def account_qqs(root: Path) -> list[str]:
    found = []
    for path in config_dir(root).glob("onebot_*.json"):
        match = re.fullmatch(r"onebot_(\d{5,12})", path.stem)
        if match:
            found.append(match.group(1))
    return sorted(set(found))


def detect_account(root: Path, owner_qq: str = "", known_qq: str = "") -> dict:
    """认出桌面 QQ 里登录的小号；排除主人自己的号。"""
    qqs = account_qqs(root)
    if owner_qq:
        qqs = [qq for qq in qqs if qq != str(owner_qq)]
    if known_qq and str(known_qq) in qqs:
        return {"qq": str(known_qq), "candidates": qqs}
    if len(qqs) == 1:
        return {"qq": qqs[0], "candidates": qqs}
    return {"qq": None, "candidates": qqs}


def remove_account_config(root: Path, qq: str) -> None:
    if qq:
        account_path(root, qq).unlink(missing_ok=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _local_zip(root: Path, boot: Path | None) -> Path | None:
    for folder in (Path(root), *(Path(root) / name for name in ZIP_DIRS[1:]),
                   Path(boot) if boot else None, (Path(boot) / "downloads") if boot else None):
        if not folder:
            continue
        for path in sorted(folder.glob("SnowLuma-*.zip")):
            if path.is_file():
                return path
    return None


def _download(dest: Path, log) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    partial = dest.with_suffix(dest.suffix + ".part")
    last = ""
    for url in URLS:
        try:
            log(f"下载 SnowLuma：{url}")
            request = urllib.request.Request(url, headers={"User-Agent": "DaFeiYu-OneClick"})
            with urllib.request.urlopen(request, timeout=60) as response, partial.open("wb") as out:
                total = int(response.headers.get("Content-Length") or 0)
                done = 0
                while True:
                    chunk = response.read(256 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
                    done += len(chunk)
                    if total and done * 100 // total != last:
                        last = done * 100 // total
                        log(f"SnowLuma 已下载 {done / 1048576:.0f}/{total / 1048576:.0f} MB")
            partial.replace(dest)
            return dest
        except (urllib.error.URLError, OSError, ValueError) as exc:
            log(f"这个地址没下动：{type(exc).__name__}")
            partial.unlink(missing_ok=True)
    raise SnowLumaError(
        "没下载到 SnowLuma。请用浏览器打开 https://github.com/SnowLuma/SnowLuma/releases 下载 "
        f"{ASSET}，放到安装目录（或安装目录\\downloads）里，再点「重试」。")


def _extract_zip(src: Path, dest: Path) -> None:
    dest = Path(dest).absolute()
    if dest.is_symlink() or dest.is_junction():
        raise SnowLumaError("安装目录是链接，无法安全解压 SnowLuma。")
    base = dest.resolve()
    with zipfile.ZipFile(src) as archive:
        infos = []
        for info in archive.infolist():
            name = info.filename.replace("\\", "/")
            parts = name.rstrip("/").split("/")
            if (name.startswith("/") or any(part in ("", ".", "..") for part in parts)
                    or info.external_attr & 0o170000 == 0o120000):  # 符号链接
                raise SnowLumaError(f"SnowLuma 压缩包里有不安全的路径：{info.filename}")
            infos.append((info, parts, name.endswith("/")))
        tops = {parts[0] for _, parts, _ in infos}
        strip = len(tops) == 1 and all(len(parts) > 1 or is_dir for _, parts, is_dir in infos)
        for info, parts, is_dir in infos:
            parts = parts[1:] if strip else parts
            out = dest
            for part in parts:
                out /= part
            if not out.resolve().is_relative_to(base):
                raise SnowLumaError(f"SnowLuma 压缩包越界：{info.filename}")
            if is_dir:
                out.mkdir(parents=True, exist_ok=True)
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as reader, out.open("wb") as writer:
                shutil.copyfileobj(reader, writer)


def ensure_installed(root: Path, boot: Path | None, log=lambda _m: None) -> Path:
    """已经装好就直接用；没有就找本地 zip，再没有就下载。"""
    root = Path(root)
    base = base_dir(root)
    if installed(root):
        return base
    source = _local_zip(root, boot)
    if source is None:
        target = root / ".tmp" / ASSET
        if not target.exists():
            source = _download(target, log)
        else:
            source = target
    log(f"校验 SnowLuma：{source.name}")
    digest = _sha256(source)
    if SHA256 and digest != SHA256:
        source.unlink(missing_ok=True)
        raise SnowLumaError(f"SnowLuma 压缩包校验不对（{digest[:12]}…）。文件已删除，请重新下载或换一个官方包。")
    staging = root / ".tmp" / "snowluma-unpack"
    shutil.rmtree(staging, ignore_errors=True)
    try:
        _extract_zip(source, staging)
        # 有的包外面还套一层目录，找 index.mjs 所在的那层。
        folder = staging if (staging / "index.mjs").is_file() else None
        if folder is None:
            found = [p for p in staging.iterdir() if p.is_dir() and (p / "index.mjs").is_file()]
            folder = found[0] if len(found) == 1 else None
        if folder is None or not (folder / "node.exe").is_file():
            raise SnowLumaError("SnowLuma 压缩包里没找到 index.mjs 和 node.exe，包可能不完整。")
        shutil.rmtree(base, ignore_errors=True)
        base.parent.mkdir(parents=True, exist_ok=True)
        folder.replace(base)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    if not installed(root):
        raise SnowLumaError("SnowLuma 解压后文件不全，可能被杀毒软件拿走了。把安装目录加进信任区后重试。")
    log("SnowLuma 已解压完成")
    return base


def eula_path(root: Path) -> Path | None:
    for name in ("EULA.md", "PRIVACY.md"):
        path = base_dir(root) / name
        if path.is_file():
            return path
    return None


# ---------- 桌面 QQ ----------

def _registry_qq_paths() -> list[Path]:
    import winreg
    found: list[Path] = []
    hives = (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE)
    for hive in hives:
        for sub in (r"Software\Tencent\QQNT", r"Software\WOW6432Node\Tencent\QQNT"):
            try:
                with winreg.OpenKey(hive, sub) as key:
                    for value in ("InstallPath", "InstallDir", "Path", "Executable"):
                        try:
                            raw = str(winreg.QueryValueEx(key, value)[0]).strip('"')
                        except OSError:
                            continue
                        if raw:
                            path = Path(raw)
                            found.append(path if path.suffix.lower() == ".exe" else path / "QQ.exe")
            except OSError:
                pass
        for sub in (r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
                    r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"):
            try:
                with winreg.OpenKey(hive, sub) as root_key:
                    for index in range(winreg.QueryInfoKey(root_key)[0]):
                        try:
                            name = winreg.EnumKey(root_key, index)
                            with winreg.OpenKey(root_key, name) as entry:
                                display = str(winreg.QueryValueEx(entry, "DisplayName")[0])
                                if "QQ" not in display or "NapCat" in display:
                                    continue
                                location = str(winreg.QueryValueEx(entry, "InstallLocation")[0]).strip('"')
                                if location:
                                    found.append(Path(location) / "QQ.exe")
                        except OSError:
                            continue
            except OSError:
                pass
    return found


_QQ_CACHE = {"path_at": 0.0, "path": None, "run_at": 0.0, "running": False}
QQ_PATH_TTL = 10.0
QQ_RUN_TTL = 3.0


def desktop_qq_path(*, refresh: bool = False) -> Path | None:
    """找桌面 QQ。状态页会频繁调用，缓存 30 秒，装完 QQ 后点刷新也会重新查。"""
    now = time.monotonic()
    if not refresh and now - _QQ_CACHE["path_at"] < QQ_PATH_TTL:
        return _QQ_CACHE["path"]
    candidates = _registry_qq_paths()
    for env in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        base = os.environ.get(env)
        if base:
            candidates.append(Path(base) / "Tencent" / "QQNT" / "QQ.exe")
            candidates.append(Path(base) / "Programs" / "Tencent" / "QQNT" / "QQ.exe")
    found = None
    for path in candidates:
        try:
            if path.is_file():
                found = path
                break
        except OSError:
            continue
    _QQ_CACHE.update(path_at=now, path=found)
    return found


def desktop_qq_running(*, refresh: bool = False) -> bool:
    """tasklist 不算便宜，2 秒一次的登录轮询没必要每次真跑。"""
    now = time.monotonic()
    if not refresh and now - _QQ_CACHE["run_at"] < QQ_RUN_TTL:
        return _QQ_CACHE["running"]
    try:
        result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq QQ.exe", "/NH", "/FO", "CSV"],
                                capture_output=True, timeout=15, creationflags=0x08000000)
    except (OSError, subprocess.TimeoutExpired):
        _QQ_CACHE.update(run_at=now, running=False)
        return False
    out = (result.stdout or b"").decode("mbcs", "replace")
    running = bool(re.search(r'"QQ\.exe"', out, re.IGNORECASE))
    _QQ_CACHE.update(run_at=now, running=running)
    return running


def open_desktop_qq(exe: Path) -> None:
    subprocess.Popen([str(exe)], cwd=str(Path(exe).parent), close_fds=True)


# ---------- 连接状态 ----------

class _MIB_TCPROW(ctypes.Structure):
    _fields_ = [("state", wintypes.DWORD), ("local_addr", wintypes.DWORD), ("local_port", wintypes.DWORD),
                ("remote_addr", wintypes.DWORD), ("remote_port", wintypes.DWORD),
                ("pid", wintypes.DWORD)]


def _tcp_rows() -> list[tuple[int, int]]:
    """返回 (远端端口, 进程号)。只查 IPv4 已建立连接，够判断 SnowLuma 有没有连上 AstrBot。"""
    try:
        iphlpapi = ctypes.WinDLL("iphlpapi")
        size = wintypes.DWORD(0)
        iphlpapi.GetExtendedTcpTable(None, ctypes.byref(size), False, socket.AF_INET, 4, 0)
        if not size.value:
            return []
        buf = ctypes.create_string_buffer(size.value)
        if iphlpapi.GetExtendedTcpTable(buf, ctypes.byref(size), False, socket.AF_INET, 4, 0) != 0:
            return []
        count = ctypes.cast(buf, ctypes.POINTER(wintypes.DWORD))[0]
        rows = ctypes.cast(ctypes.addressof(buf) + ctypes.sizeof(wintypes.DWORD),
                           ctypes.POINTER(_MIB_TCPROW))
        result = []
        for index in range(count):
            row = rows[index]
            if row.state == 5:  # ESTABLISHED
                result.append((socket.ntohs(row.remote_port & 0xFFFF), int(row.pid)))
        return result
    except (OSError, AttributeError):
        return []


def connected_to_astrbot(root: Path, onebot_port: int) -> bool:
    try:
        from services import process_path
    except ImportError:
        return False
    expected = (base_dir(root) / "node.exe").resolve()
    for port, pid in _tcp_rows():
        if port != onebot_port:
            continue
        try:
            if process_path(pid) == expected:
                return True
        except OSError:
            continue
    return False


def login_state(root: Path, onebot_port: int, running: bool) -> dict:
    """给页面看的 SnowLuma 状态。名称沿用 NapCat 那套，前端可以复用。"""
    root = Path(root)
    if not running:
        return {"status": "starting", "account": "", "candidates": [],
                "desktop_qq": bool(desktop_qq_path()), "desktop_qq_running": desktop_qq_running()}
    found = detect_account(root)
    connected = connected_to_astrbot(root, onebot_port)
    if connected:
        status = "online"
    elif found["qq"]:
        status = "scanned"  # 认出了小号，正在等它连上 AstrBot
    elif found["candidates"]:
        status = "offline"  # 登着不止一个号，分不清哪个是小号
    else:
        status = "need_scan"  # 还没在桌面 QQ 里登录小号
    return {"status": status, "account": found["qq"] or "",
            "candidates": found["candidates"],
            "desktop_qq": bool(desktop_qq_path()), "desktop_qq_running": desktop_qq_running()}
