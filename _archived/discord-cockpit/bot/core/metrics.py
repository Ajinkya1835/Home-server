import time
import platform
import socket

import psutil


def bar(percent: float, length: int = 10) -> str:
    filled = max(0, min(length, round(percent / 100 * length)))
    return "█" * filled + "░" * (length - filled)


def get_uptime() -> str:
    seconds = int(time.time() - psutil.boot_time())
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)
    return f"{days}d {hours}h {minutes}m"


def get_cpu():
    return {
        "percent": psutil.cpu_percent(interval=1),
        "load": psutil.getloadavg(),
        "cores": psutil.cpu_count(),
    }


def get_memory():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "percent": mem.percent,
        "used_gb": mem.used / 1024**3,
        "total_gb": mem.total / 1024**3,
        "swap_percent": swap.percent,
    }


def get_disks():
    mounts = [("/", "Root (sdb2)"), ("/mnt/hdd1", "HDD (encrypted)")]
    disks = []
    for path, label in mounts:
        try:
            usage = psutil.disk_usage(path)
            disks.append({
                "label": label,
                "percent": usage.percent,
                "used_gb": usage.used / 1024**3,
                "total_gb": usage.total / 1024**3,
            })
        except FileNotFoundError:
            continue
    return disks


def get_temps():
    try:
        temps = psutil.sensors_temperatures()
    except AttributeError:
        return None

    core_temps = temps.get("coretemp-isa-0000") or temps.get("coretemp")
    if not core_temps:
        return None

    readings = [t.current for t in core_temps if t.current]
    if not readings:
        return None

    return {
        "avg": sum(readings) / len(readings),
        "max": max(readings),
    }


def get_host_info():
    return {
        "hostname": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
        "uptime": get_uptime(),
    }
