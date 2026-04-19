import logging
import os
from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException, NetmikoAuthenticationException

class NetworkDevice:
    def __init__(self, hostname, host, device_type, group):
        self.hostname = hostname
        self.host = host
        self.device_type = device_type
        self.group = group
        self.username = None
        self.password = None
        self.secret = None
        self.netconnect = None
        self.logger = logging.getLogger(f"{__name__}.{hostname}")
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            directory = "logs"
            if not os.path.isdir(directory):
                os.makedirs(directory)
            
            file_hanlder = logging.FileHandler(f"logs/{hostname}.log")
            file_hanlder.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            file_hanlder.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                "%(levelname)s - %(message)s"
            )
            console_handler.setFormatter(console_formatter)

            self.logger.addHandler(file_hanlder)
            self.logger.addHandler(console_handler)

    def connect(self):
        self.logger.info(f"Attempting to connect to {self.hostname}")
        connection_established = False
        connection_attempts = 0
        max_retries = 2

        while not connection_established and connection_attempts < max_retries:
            try:
                self.net_connect = ConnectHandler(
                    device_type=self.device_type,
                    host=self.host,
                    username=self.username,
                    password=self.password,
                    secret=self.secret
                )
                self.logger.info(f"Successfully connected to {self.hostname}")
                connection_established = True
                return connection_established
            except NetmikoAuthenticationException:
                self.logger.info("Invalid credentials")
                return connection_established
            except NetmikoTimeoutException:
                self.logger.info(f"Unable to connect to {self.host}")
                connection_attempts += 1
            if connection_attempts >= max_retries:
                self.logger.error(f"Unable to connect to {self.host} after {max_retries} attempts")

    def get_config(self):
        device_commands = {
            "cisco_ios": {
                "get_config": "show running-config",
            },
            "adtran_os": {
                "get_config": "show running-config",
            },
            "juniper_junos": {
                "get_config": "show configuration",
            }
        }
        if self.net_connect is not None:
            try:
                if self.device_type == "adtran_os" or self.device_type == "cisco_ios":
                    self.net_connect.enable()
                get_config_cmd = device_commands[self.device_type]["get_config"]
                self.logger.debug(f"Sending: {get_config_cmd}")
                output = self.net_connect.send_command(get_config_cmd)
                return output # returns the output to commandmanager.py so it can be saved to file           
            except Exception as error:
                self.logger.error(f"Error with config retreival from {self.hostname}: {error}")
                return None
    
    def send_commands(self, device_commands):
        commands_output = []

        for command_type, command_list in device_commands.items():
            if command_type == "pre_check" or command_type == "post_check":
                if self.device_type == "adtran_os" or self.device_type == "cisco_ios":
                    self.net_connect.enable()
                for command in command_list:
                    try:
                        self.logger.debug(f"Sending: {command}")
                        output = self.net_connect.send_command(command)
                        commands_output.append(output)
                        self.logger.info(f"Output: {output}")
                    except Exception as error:
                        self.logger.error(f"Error: {error}")
                        commands_output.append(error)
            if command_type == "configuration":
                try:
                    self.logger.debug(f"Sending: {command_list}")
                    output = self.net_connect.send_config_set(command_list)
                    commands_output.append(output)
                    self.logger.info(f"Output: {output}")
                except Exception as error:
                    self.logger.error(f"Error: {error}")
                    commands_output.append(error)

    def disconnect(self):
        self.logger.info(f"Disconnecting from {self.hostname}...")
        self.net_connect.disconnect()
'''
device.py functionality

You can do the following to/with the device:

Send commands
Log outputs
Get configs
Connect
Disconnect
'''
'''
device_commands = {
    "pre_check": [
        "show ip interface brief",
        "show version",
        "show arp"
    ],
    "configuration": [
        "vlan 100",
        "name test-vlan"
    ],
    "post_check": [
        "show vlan brief",
        "write memory"
    ]
}
'''