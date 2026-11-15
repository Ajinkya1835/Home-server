import json, time, urllib.request, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

PROM = "http://prometheus:9090"

def q(expr):
    try:
        url = PROM + "/api/v1/query?query=" + urllib.parse.quote(expr)
        return json.load(urllib.request.urlopen(url, timeout=3))["data"]["result"]
    except Exception:
        return None

def val(expr):
    r = q(expr)
    return float(r[0]["value"][1]) if r else None

def fmt(v, suffix="", nd=0):
    return "n/a" if v is None else ("%." + str(nd) + "f%s") % (v, suffix)

def color(v, warn, crit):
    if v is None: return "#888"
    return "#f55" if v >= crit else ("#fb3" if v >= warn else "#5d5")

def cell(label, v, suffix, warn, crit):
    return ('<td class="c"><div class="l">%s</div>'
            '<div class="v" style="color:%s">%s</div></td>') % (label, color(v, warn, crit), fmt(v, suffix))

def page():
    cpu = val('100 - avg(rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100')
    mem = val('(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100')
    temp = val('max(node_hwmon_temp_celsius)')
    up = val('time() - node_boot_time_seconds')
    down = val('count(up == 0) or vector(0)')
    disks = q('100 * (1 - node_filesystem_avail_bytes{fstype=~"ext4|xfs|btrfs"} / node_filesystem_size_bytes{fstype=~"ext4|xfs|btrfs"})') or []
    alerts = q('ALERTS{alertstate="firing"}') or []

    days = "n/a" if up is None else "%dd %dh" % (up // 86400, (up % 86400) // 3600)
    disk_rows = ""
    seen = set()
    for d in disks:
        m = d["metric"].get("mountpoint", "?")
        if m in seen: continue
        seen.add(m)
        p = float(d["value"][1])
        disk_rows += '<tr><td class="l2">%s</td><td class="r" style="color:%s">%.0f%%</td></tr>' % (m, color(p, 80, 90), p)
    if not disk_rows:
        disk_rows = '<tr><td class="l2">no disk data</td><td></td></tr>'

    if alerts:
        al = "".join('<div class="bad">%s</div>' % a["metric"].get("alertname", "alert") for a in alerts)
    else:
        al = '<div class="ok">No active alerts</div>'

    html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<meta http-equiv="refresh" content="10">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Server</title>
<style>
body{background:#0b1120;color:#eee;font-family:sans-serif;margin:0;padding:12px}
h1{font-size:34px;margin:0 0 10px 0}
table{width:100%%;border-collapse:collapse}
.c{width:25%%;text-align:center;padding:12px 4px;background:#151d33;border:4px solid #0b1120}
.l{font-size:16px;color:#9ab}.v{font-size:36px;font-weight:bold}
.l2{font-size:22px;padding:6px}.r{font-size:22px;text-align:right;padding:6px}
.ok{color:#5d5;font-size:22px;padding:10px}.bad{color:#f55;font-size:26px;padding:6px}
.t{font-size:18px;color:#9ab;padding-top:10px}
</style></head><body>
<h1>Ajinkya Home Lab &nbsp; <span style="color:#9ab;font-size:26px">%s</span></h1>
<table><tr>%s%s%s%s</tr></table>
<table style="margin-top:8px">%s</table>
<table style="margin-top:8px"><tr><td class="c"><a href="http://192.168.29.106:6080/vnc.html?autoconnect=true&resize=scale" style="color:#8cf;font-size:26px;text-decoration:none">Desktop</a></td><td class="c"><a href="http://192.168.29.106:3030" style="color:#8cf;font-size:26px;text-decoration:none">Homepage</a></td></tr></table><h2 style="font-size:24px;margin:14px 0 4px 0">Alerts</h2>%s
<div class="t">Uptime %s &nbsp; | &nbsp; Targets down: %s</div>
</body></html>""" % (
        time.strftime("%H:%M  %a %d %b"),
        cell("CPU", cpu, "%", 70, 90), cell("RAM", mem, "%", 80, 90),
        cell("TEMP", temp, "&deg;C", 70, 80), cell("DOWN", down, "", 1, 1),
        disk_rows, al, days, fmt(down))
    return html.encode()

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = page()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

HTTPServer(("0.0.0.0", 8080), H).serve_forever()
