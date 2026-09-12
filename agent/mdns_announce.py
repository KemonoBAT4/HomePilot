import socket
import uuid

from zeroconf import ServiceInfo, Zeroconf

SERVICE_TYPE = "_homepilot._tcp.local."


def _local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


def _local_mac() -> str:
    mac_int = uuid.getnode()
    return ":".join(f"{(mac_int >> ele) & 0xff:02x}" for ele in range(40, -8, -8))


def start_announce(device_id: str, pairing_port: int):
    hostname = socket.gethostname()
    ip = _local_ip()

    info = ServiceInfo(
        SERVICE_TYPE,
        f"{device_id}.{SERVICE_TYPE}",
        addresses=[socket.inet_aton(ip)],
        port=pairing_port,
        properties={
            "device_id": device_id,
            "hostname": hostname,
            "os_type": "windows",
            "mac": _local_mac(),
        },
        server=f"{hostname}.local.",
    )

    zc = Zeroconf()
    zc.register_service(info)
    return zc, info


def stop_announce(zc: Zeroconf, info: ServiceInfo) -> None:
    zc.unregister_service(info)
    zc.close()
