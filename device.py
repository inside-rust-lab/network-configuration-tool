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

    def connect(self):
        print(f"Attempting to connect to {self.hostname}...")
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
                print(f"Successfully connected to {self.hostname}")
                connection_established = True
                return connection_established
            except NetmikoAuthenticationException:
                print("Invalid credentials")
                return connection_established
            except NetmikoTimeoutException:
                print(f"Unable to connect to {self.host}")
                connection_attempts += 1
            if connection_attempts >= max_retries:
                print(f"Unable to connect to {self.host} after {max_retries} attempts")

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
                output = self.net_connect.send_command(get_config_cmd)
                return output              
            except:
                print(f"Unable to retrieve config file from {self.hostname}")
                return None
    
    def send_commands(self, device_commands):
        commands_output = []

        for command_type, command_list in device_commands.items():
            if command_type == "pre_check" or command_type == "post_check":
                if self.device_type == "adtran_os" or self.device_type == "cisco_ios":
                    self.net_connect.enable()
                for command in command_list:
                    try:
                        output = self.net_connect.send_command(command)
                        commands_output.append(output)
                        print(output)
                    except Exception as error:
                        print(f"Error: {error}")
                        commands_output.append(error)
            if command_type == "configuration":
                try:
                    output = self.net_connect.send_config_set(command_list)
                    commands_output.append(output)
                    print(output)
                except Exception as error:
                    print(f"Error: {error}")
                    commands_output.append(error)

    def disconnect(self):
        print(f"Disconnecting from {self.hostname}...")
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