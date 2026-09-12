
import socket

def send_magic_packet(mac_address: str, broadcast_ip: str = "255.255.255.255", port: int = 9) -> None:
    """
    #### DESCRIPTION:
    Sends a magic packet wake-on-lan to the MAC address indicated.

    #### PARAMETERS:
    - mac_address: The MAC address of the device to wake up.
    - broadcast_ip: The IP address to send the magic packet to. Defaults to "255.255.255.255".
    - port: The port to send the magic packet to. Defaults to 9.

    #### RETURNS:
    None
    """

    mac_bytes    : bytes = bytes.fromhex(mac_address.replace(":", "").replace("-", ""))
    magic_packet : bytes = b"\xff" * 6 + mac_bytes * 16

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, (broadcast_ip, port))
    # #endwith
# #enddef send_magic_packet
