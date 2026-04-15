from commandmanager import CommandManager

cm = CommandManager()
cm.send_commands()

'''
To do:
More error handling
I want to make it so you don't have to have multiple groups in the commands.yaml file
Basically it only connects to the groups that are configured in commands.yaml
logging
Simultaneous configuration
Add device roles
    Make it so you can configure all cisco switches, all juniper firewalls, all cisco routers
Add functionality to configure individual devices too
Build all of this into a docker container
'''