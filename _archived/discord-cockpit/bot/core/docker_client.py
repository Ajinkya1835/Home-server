import docker

_client = None
def container_details_for_ai():
    containers = list_containers()
    lines = []
    for c in containers:
        lines.append(f"{c['name']}: {c['status']}" + (f" (health: {c['health']})" if c["health"] else ""))
    return "\n".join(lines)

def get_client():
    global _client
    if _client is None:
        _client = docker.from_env()
    return _client


def list_containers():
    client = get_client()
    containers = client.containers.list(all=True)

    result = []
    for c in containers:
        health = None
        state = c.attrs.get("State", {})
        if "Health" in state:
            health = state["Health"].get("Status")

        result.append({
            "name": c.name,
            "status": c.status,
            "health": health,
            "image": c.image.tags[0] if c.image.tags else c.image.short_id,
        })
    return result


def container_summary():
    containers = list_containers()
    total = len(containers)
    running = sum(1 for c in containers if c["status"] == "running")
    unhealthy = sum(1 for c in containers if c["health"] == "unhealthy")
    stopped = sum(1 for c in containers if c["status"] != "running")
    return {
        "total": total,
        "running": running,
        "stopped": stopped,
        "unhealthy": unhealthy,
    }
def get_container(name: str):
    client = get_client()
    return client.containers.get(name)


def container_stats(name: str):
    container = get_container(name)
    stats = container.stats(stream=False)

    cpu_delta = (
        stats["cpu_stats"]["cpu_usage"]["total_usage"]
        - stats["precpu_stats"]["cpu_usage"]["total_usage"]
    )
    system_delta = (
        stats["cpu_stats"]["system_cpu_usage"]
        - stats["precpu_stats"].get("system_cpu_usage", 0)
    )
    num_cpus = stats["cpu_stats"].get("online_cpus", 1)

    cpu_percent = 0.0
    if system_delta > 0 and cpu_delta > 0:
        cpu_percent = (cpu_delta / system_delta) * num_cpus * 100.0

    mem_usage = stats["memory_stats"].get("usage", 0)
    mem_limit = stats["memory_stats"].get("limit", 1)
    mem_percent = (mem_usage / mem_limit) * 100.0 if mem_limit else 0.0

    return {
        "cpu_percent": cpu_percent,
        "mem_usage_mb": mem_usage / 1024**2,
        "mem_limit_mb": mem_limit / 1024**2,
        "mem_percent": mem_percent,
    }


def container_logs(name: str, tail: int = 30) -> str:
    container = get_container(name)
    logs = container.logs(tail=tail).decode("utf-8", errors="replace")
    return logs


def restart_container(name: str):
    container = get_container(name)
    container.restart(timeout=10)


def stop_container(name: str):
    container = get_container(name)
    container.stop(timeout=10)


def start_container(name: str):
    container = get_container(name)
    container.start()
