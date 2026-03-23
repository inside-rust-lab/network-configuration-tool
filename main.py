from backupmanager import BackupManager
import argparse

parser = argparse.ArgumentParser("nbtool", "Backup network device(s)")
parser.add_argument("-b", "--backup", 
                    metavar="HOSTNAME", 
                    type=str, 
                    help="Backup the config of a host")
parser.add_argument("-a", "--backup-all",
                    action="store_true", 
                    help="Backup all devices in devices.json")
parser.add_argument("-l", "--list-devices", 
                    action="store_true",
                    help="List all devices configed in devices.json")
parser.add_argument("-v", "--list-vendors", 
                    action="store_true",
                    help="List the unique vendors for all devices configured in devices.json")

args = parser.parse_args()
backup_manager = BackupManager()

if not backup_manager.json_file_error:
    if args.backup:
        hostname = args.backup
        backup_manager.backup_device(hostname)

    if args.backup_all:
        backup_manager.backup_all()

    if args.list_devices:
        print("Listing all devices:\n")
        for device in backup_manager.devices:
            print(f"Hostname: {device.hostname}")
            print(f"Host: {device.host}")
            print(f"Vendor: {device.device_type}\n")

    if args.list_vendors:
        print("Listing all vendors:\n")
        vendors = set()
        for device in backup_manager.devices:
            vendors.add(device.device_type)
        print(vendors)