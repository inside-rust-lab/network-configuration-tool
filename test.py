import yaml

with open("devices.yaml", "r") as file:
    devices = yaml.safe_load(file)

with open("commands.yaml", "r") as file:
    commands = yaml.safe_load(file)

print(devices)
print(devices["cisco"])
print(devices["cisco"]["SW-LAB-01"])

print(commands)