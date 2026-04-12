import datetime
import os
import getpass
import yaml
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
                        device_data["device_type"],
                        group
                    )
                )
        return network_devices
    
    def save_config(self, device):
        successful_connection = device.connect()
        if not successful_connection:
            return

        config = device.get_config()

        directory = "backups"
        if not os.path.isdir(directory):
            os.makedirs(directory)

        current_time = datetime.datetime.now()
        current_time_formatted = current_time.strftime("%m-%d-%y_%H:%M:%S")
        file_name = f"{directory}/{device.hostname}_{current_time_formatted}.conf"
        with open(file_name, "w") as file:
            file.write(config)
            print(f"Config was saved as ./{file_name}")
            
        device.disconnect()
        return
    
    def send_commands(self):
        self.get_login_credentials()
        network_devices = self.devices

        if network_devices is None:
            return

        for device in network_devices:
            successful_connection = device.connect()
            if successful_connection:
                device.send_commands()
                device.disconnect()
'''
CommandManager functionality:

Handles user credentials
Send commands to a single group
Send commands to all groups
Creates and manages NetworkDevice objects
'''

'''
Does device.py load the commands from the yaml file or command manager?
device.py would?
commandmanager would cycle through the device objects, tell the device to send the commands from its assigned group

'''