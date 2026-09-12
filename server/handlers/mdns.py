
from typing import Dict, Optional
from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

SERVICE_TYPE = "_homepilot._tcp.local."

# Registro in memoria: device_id -> info del dispositivo visto in LAN.
# Non contiene nulla di sensibile, solo hostname/os/ip/porta.
discovered_devices: Dict[str, dict] = {}


def _decode_properties(info) -> dict:
    return {k.decode(): v.decode() for k, v in (info.properties or {}).items() if v is not None}
# #enddef _decode_properties

class HomePilotListener(ServiceListener):
    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if not info:
            return
        # #endif

        properties = _decode_properties(info)
        device_id = properties.get("device_id")
        if not device_id:
            return
        # #endif

        addresses = info.parsed_addresses()
        discovered_devices[device_id] = {
            "device_id" : device_id,
            "hostname"  : properties.get("hostname", info.server or name),
            "os_type"   : properties.get("os_type"),
            "mac"       : properties.get("mac"),
            "ip"        : addresses[0] if addresses else None,
            "port"      : info.port,
        }
    # #enddef add_service

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        properties = _decode_properties(info) if info else {}
        device_id = properties.get("device_id")

        if device_id:
            discovered_devices.pop(device_id, None)
        # #endif
    # #enddef remove_service

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.add_service(zc, type_, name)
    # #enddef update_service
# #endclass HomePilotListener

_zeroconf_instance: Optional[Zeroconf] = None

def start_discovery() -> None:
    global _zeroconf_instance
    _zeroconf_instance = Zeroconf()
    listener = HomePilotListener()
    ServiceBrowser(_zeroconf_instance, SERVICE_TYPE, listener)
# #enddef start_discovery

def stop_discovery() -> None:
    global _zeroconf_instance

    if _zeroconf_instance:
        _zeroconf_instance.close()
        _zeroconf_instance = None
    # #endif
# #enddef stop_discovery
