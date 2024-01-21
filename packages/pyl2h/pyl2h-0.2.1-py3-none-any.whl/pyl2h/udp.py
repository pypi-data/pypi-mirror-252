"""UDP functionality for internal communication with devices."""

import socket

class UDPServer:
    """UDP Listener/Server functionality"""
    def __init__(self) -> None:
        self.devices = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("", 35932))

    def set_discovered_devices(self, devices):
        """Add known devices that have been discovered (i.e. through cloud)"""
        for dev in devices:
            mac = dev['mac']
            encoded_mac = b''

            for i in range(0, len(mac), 2):
                byte = mac[i:i+2]
                encoded_mac += int(byte, 16).to_bytes(1, 'big')

            dev['mac'] = encoded_mac
            self.devices[encoded_mac] = dev
            message = b'\xa1\x00'+encoded_mac+b'\x00\x07\x00\x01\x00\x00\x00\x00\x23'
            self.send_message('255.255.255.255', message)
        print(f'Sent discovery for {len(devices)} devices')

    def decode_status_broadcast(self, data, ip):
        """Decode status update broadcasted by device"""
        mac = data[2:8]
        channel = data[len(data)-2]
        is_on = not data[len(data)-1] == 0

        state = {}
        state["mac"] = mac
        state["channel"] = channel
        state["status"] = is_on
        state["ip"] = ip

        return state

    def process_message(self, data, address):
        """Process message received on UDP socket"""
        ip = address[0]
        new_state = self.decode_status_broadcast(data, ip)
        mac = new_state["mac"]


        old_state = self.devices[mac] if mac in self.devices else {}
        old_state["mac"] = new_state["mac"]
        if "channels" not in old_state:
            old_state["channels"] = {}
        old_state["channels"][new_state["channel"]] = new_state["status"]
        old_state["ip"] = ip

        self.devices[mac] = old_state

        return old_state

    def send_message(self, ip, message):
        """Send a message to a device or Broadcast"""
        self.sock.sendto(message, (ip, 35932))

    def set_status(self, ip, channel: int, state):
        """Change the status of a device by sending a UDP multicast to it"""
        print(f'Setting state {state} on channel {channel} for device {ip}')
        state_byte = b'\xff' if state else b'\x00'
        channel_byte = bytes([channel])
        for dev in self.devices.values():
            if dev["ip"] == ip:
                mac = dev["mac"]
                message = b'\xa1\x04'+mac+b'\x00\x09\x01\xf2\x02\xd1\x71\x50\x01'+channel_byte+state_byte
                self.send_message(ip, message)
                break

    def get_devices(self):
        """Get the currently known list of devices"""
        return self.devices

    def listen(self, subscriber=None):
        """Start listening for device Updates on the UDP procotol"""
        while True:
            data, addr = self.sock.recvfrom(1024)
            device_status = self.process_message(data, addr)
            if device_status is not None and subscriber is not None:
                subscriber(device_status)
