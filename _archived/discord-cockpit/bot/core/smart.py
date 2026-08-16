import re
import subprocess

DRIVES = [
    {"device": "/dev/sda", "label": "WD Scorpio Blue (HDD, encrypted)", "type": None},
    {"device": "/dev/sdb", "label": "System SSD", "type": "sat"},
]


def _run_smartctl(device: str, dtype: str = None) -> str:
    cmd = ["smartctl", "-a"]
    if dtype:
        cmd.extend(["-d", dtype])
    cmd.append(device)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    return result.stdout


def parse_smart(device: str, dtype: str = None) -> dict:
    output = _run_smartctl(device, dtype)

    health_match = re.search(r"SMART overall-health self-assessment test result:\s*(\w+)", output)
    health = health_match.group(1) if health_match else "UNKNOWN"

    def attr(attr_id_or_name: str):
        for line in output.splitlines():
            if attr_id_or_name in line and re.match(r"^\s*\d+", line):
                parts = line.split()
                if len(parts) >= 10:
                    return parts[-1]
        return None

    return {
        "device": device,
        "health": health,
        "reallocated_sectors": attr("Reallocated_Sector_Ct"),
        "pending_sectors": attr("Current_Pending_Sector"),
        "uncorrectable_sectors": attr("Offline_Uncorrectable"),
        "temp_c": attr("Temperature_Celsius"),
    }


def get_all_smart():
    results = []
    for drive in DRIVES:
        try:
            data = parse_smart(drive["device"], drive.get("type"))
            data["label"] = drive["label"]
            results.append(data)
        except subprocess.TimeoutExpired:
            results.append({
                "device": drive["device"], "label": drive["label"],
                "health": "ERROR", "error": "timed out — device may not support SMART over this interface",
            })
        except Exception as e:
            results.append({"device": drive["device"], "label": drive["label"], "health": "ERROR", "error": str(e)})
    return results
