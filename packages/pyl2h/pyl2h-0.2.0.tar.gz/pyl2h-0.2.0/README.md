# Link2Home Protocoll implementation

This projects implements (part of) the propretiary [Link2Home](https://www.l2h-rev.de/) communication protocol for monitoring and controlling devices from third party projects.

:warning: This is under development and in very early stage!
:warning: This project is based on reverse engineering and is neither associated nor supported by the offical product. This is mere a workaround to the missing of an official open API or third party integrations

# Basics
The Link2Home protocol is relying on two major parts:
1. Authenticated HTTP Calls to a backend hosted by the vendor. This is mainly for user profile portability, storing device metadata and discovery
2. Unauthenticated UDP Broad- and Unicasts for changing device state and announcing changes

This project currently relies solely on 2. and is operating solely within the local network.

# Usage

With importing the `UDPServer` class, you've are able to access the data stream of device change updates, the current directory of known devices and sending command messages

```
from l2h import UDPServer

server = UDPServer()

def deviceCallback(deviceStatus):
    print("New Device Update: {}".format(deviceStatus))

devices = server.getDevices()
server.setStatus("192.168.1.3", 1, True)

server.listen(deviceCallback)
```

Devices will be auto-discovered with their first state switch (i.e. when they are sending their first status update after the program has started), only after that, the library will be able to successfully communicate with the device. It is recommended that you trigger the devices manually (either by their physical buttons or via the official app) after having the server up to make autodiscovery work faster. Please Note: Apps currently also show up as devices.

`main.py` is also offering a CLI mode that will log status updates of devices and allow to alternate states of a device by it's IP supplied as an argument:

```
python main.py --ip 192.168.1.3
```

# Development

As of now, this library has been developed and tested solely with a EMQ303WF-1 smart socket