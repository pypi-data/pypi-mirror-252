"""CLI functionality for debugging and testing."""

import argparse
import asyncio
from time import sleep
from .udp import UDPServer
from .cloud_client import CloudClient

server = UDPServer()

def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""

    parser = argparse.ArgumentParser(
        description="Matter Controller Server using WebSockets."
    )
    parser.add_argument(
        "--ip",
        type=str,
        default=None,
        help="IP of the device to be used for testing. Will Flip-Flop Channel 1 every Minute",
    )

    parser.add_argument(
        "--user",
        type=str,
        default=None,
        help="Username for Link2Home Cloud/App to use for discovery",
    )

    parser.add_argument(
        "--password",
        type=str,
        default=None,
        help="Password for Link2Home Cloud/App to use for discovery",
    )

    parser.add_argument(
        "--sign",
        type=str,
        default=None,
        help="Password sign as captured from original requests."\
        " For veryfing internal logic during debugging",
    )

    arguments = parser.parse_args()

    return arguments

def device_callback(device_status):
    """Callback for new status updates by devices."""
    print(f'New Device Update: {device_status}')

def monitor_updates():
    """Entrypoint for starting to listen for device updates"""
    server.listen(device_callback)

def main() -> int:
    """Main entrypoint for CLI based operation and example for usage"""
    args = get_arguments()

    cloud = CloudClient()

    ip = args.ip

    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, monitor_updates)
    print(args)
    if args.user is not None and args.password is not None:
        cloud.login(args.user, args.password)
        devices = cloud.list_devices()
        print(f"discovered devices from cloud: {devices}")
        server.set_discovered_devices(devices)

    while True:
        devices = server.get_devices()
        print("Devices:")
        for d in devices.items():
            print(d)

        if ip is not None and ip in devices:
            dev = devices[ip]
            new_state = not dev["channels"][1]
            print(f'Switching device {ip} to {new_state}')
            server.set_status(ip, 1, new_state)

        sleep(60)

def create_sign() -> bool:
    """Test request signature against control value (e.g. from intercepted communication)"""
    args = get_arguments()
    cloud = CloudClient()

    data = {
        "appName": "Link2Home",
        "appType": "2",
        "appVersion": "1.1.1",
        "password": cloud.hash_password(args.password),
        "phoneSysVersion": "iOS 17.1.2",
        "phoneType": "iPad13,8",
        "username": args.user,
    }

    calculated_sign = cloud.get_sign(data)

    print("")
    print(f'Expected sign (control): {args.sign}')
    print("")
    print(f'Calculated sign: {calculated_sign}')
    print("")

    if calculated_sign == args.sign:
        print("Success! Calctulated sign equals control sign")
        return True

    print("Failed! Calculated sign differs from control sign")
    return False
