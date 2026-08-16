import os

ADMIN_IDS = {
    int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip()
}

ROOT_MOUNT = "/"
HDD_MOUNT = "/mnt/hdd1"

PROTECTED_CONTAINERS = {"discord-cockpit"}


def is_admin(user_id: int) -> bool:
    if not ADMIN_IDS:
        return True  # no admins configured yet, don't lock everyone out
    return user_id in ADMIN_IDS
