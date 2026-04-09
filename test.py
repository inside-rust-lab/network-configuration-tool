import yaml
import getpass
from device import NetworkDevice

class CommandManager:
    def __init__(self):
        self.yaml_file_error = None
        self.devices = self.load_devices()
    
    def get_login_credentials(self):
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        secret = getpass.getpass("Enable password: ")
        credentials = {
            "username": username,
            "password": password,
            "secret": secret
        }
        for device in self.devices:
            device.username = credentials["username"]
            device.password = credentials["password"]
            device.secret = credentials["secret"]
    
    def load_devices(self):
        network_devices = [] # list of NetworkDevice objects
        yaml_file_name = "devices.yaml"
        
        try:
            with open(yaml_file_name, "r") as file:
                devices_yaml_data = yaml.safe_load(file)
                self.yaml_file_error = False
        except FileNotFoundError:
            print(f"File name {yaml_file_name} was not found")
            self.yaml_file_error = True
            return
        except yaml.YAMLError:
            print(f"YAML data in {yaml_file_name} is not formatted properly")
            self.yaml_file_error = True
            return
        except PermissionError:
            print(f"You do not have permissions to open {yaml_file_name}")
            self.yaml_file_error = True
            return
        
        for group, device_dict in devices_yaml_data.items():
            for hostname, device_data in device_dict.items():
                network_devices.append(
                    NetworkDevice(
                        hostname,
                        device_data["host"],
                        device_data["device_type"]
                    )
                )
        return network_devices

command_manager = CommandManager()
print(command_manager.devices)
'''
devices = {
    "cisco": {
        "SW-LAB-01": {
            "host": "10.0.0.2",
            "device_type": "cisco_ios"
        }
    },
    "juniper": {
        "FW-LAB-01": {
            "host": "10.0.0.1",
            "device_type": "juniper_junos"
        }
    },
    "adtran": {
        "AD-LAB-01": {
            "host": "192.168.20.1",
            "device_type": "adtran_os"
        }
    }    
}
'''
'''
cisco:
  SW-LAB-01:
    host: 10.0.0.2

junhoster:
  FW-LAB-01:
    host: 10.0.0.1

adtran:
  AD-LAB-01:
    host: 192.168.254.1
'''