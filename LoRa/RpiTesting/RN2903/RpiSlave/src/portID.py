import serial.tools.list_ports

# Find all available COM ports
available_ports = list(serial.tools.list_ports.comports())

for item in available_ports:
    print(item)
