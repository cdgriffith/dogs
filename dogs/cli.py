from pathlib import Path
from itertools import count

import cutie
from appdirs import user_config_dir
from box import Box

from dogs.dogs import DOGS, find_droplets, find_snapshots

user_config_file = Path(user_config_dir(appname="DOGS", roaming=True, appauthor=False), "config.yaml")
local_config_file = Path("config.yaml")


def find_config_file():
    if user_config_file.exists() and local_config_file.exists():
        print("Config files were found in both local and user directory, which do you want to use?")
        opts = [user_config_file, local_config_file]
        return opts[cutie.select(opts)]
    elif local_config_file.exists():
        print("Using local config file")
        return local_config_file
    elif user_config_file.exists():
        print("Using stored config file")
        return user_config_file
    else:
        raise Exception("No config file found!")


def stats(server, config, details=False):
    si = config.servers[server]
    server_name = si.name
    tabbed = "\n    "
    print(f"\nServer: {server_name}")
    print(f"    region: {si.region}")
    print(f"    size: {si.size}")
    print(f"    maximum snapshots: {si.snapshot_max}\n")
    if details:
        drops = find_droplets(server_name, config)
        if drops:
            print(" Droplets:")
            print(f"    {tabbed.join(drops)}")
        snaps = find_snapshots(server_name, config)
        if snaps:
            print(" Snapshots:")
            print(f"    {tabbed.join(snaps)}")


def manage(config, config_file):
    """
    Allows the user to manage a server, by either turning it on, shutting it down,
    viewing its info, or cleaning up old snapshots. The user can then choose to
    manage more or exit.
    """
    server_continue = False
    for _ in count():
        if not server_continue:
            print("\nWhich server do you want to manage?")
            opts = [s.name for s in config.servers] + ['Exit']
            selection = cutie.select(options=opts)
            if selection == len(opts) - 1:
                break
            server_index = selection
            stats(server_index, config, details=False)
        else:
            server_index = server_continue
        server_continue = False
        server_name = config.servers[server_index].name

        dogs = DOGS(server_name, config_file)
        if dogs.droplet:
            print(f"Running: {dogs.droplet.ip_address}")
        else:
            print("Currently not running")

        # Actions
        actions = [
            "View Server Info",
            "Cleanup Old Snapshots",
            "Cancel"
        ]
        if dogs.droplet:
            actions.insert(0, "Shutdown")
        else:
            actions.insert(0, "Turn On")

        print("\nManage:")
        action = actions[cutie.select(actions, selected_index=0)]

        if action == "Turn On":
            print("\nTurning droplet on\n")
            dogs.create()
        elif action == "Shutdown":
            print("\nShutting down droplet\n")
            dogs.destroy()
        elif action == "Cleanup Old Snapshots":
            print("\nRemoving old snapshots\n")
            dogs.cleanup()
        elif action == "View Server Info":
            stats(server_index, config, details=True)
            server_continue = server_index
            continue

        print("\nWould you like to:")
        selection = cutie.select(["Manage more", "Exit"], selected_index=1)
        if selection == 0:
            continue
        else:
            break


def main():
    config_file = find_config_file()
    cfg = Box.from_yaml(filename=config_file)
    manage(cfg, config_file)


if __name__ == '__main__':
    main()
