import serial.tools.list_ports

# Get a list of all available serial ports
ports = serial.tools.list_ports.comports()

# Iterate over the ports and print information about each port
for port in ports:
    print(f"Device: {port.device}, Description: {port.description}")

