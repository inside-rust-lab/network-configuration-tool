from commandmanager import CommandManager

cm = CommandManager()
cm.send_commands()

'''
To do:
Add device roles
    Make it so you can configure all cisco switches, all juniper firewalls, all cisco routers
Add functionality to configure individual devices too
I only have a group which doesn't scale all that well
I think a single device needs to have the capability to be assigned multiple roles or have multiple tags
Examples:
wan device, access switch, core switch, switch, router, firewall, juniper, adtran, cisco etc.
How do I do this?
* shoulder shrug
Build all of this into a docker container
'''