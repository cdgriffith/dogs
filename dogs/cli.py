from pathlib import Path
from itertools import count

import cutie
from appdirs import user_config_dir
from box import Box


from dogs import DOGS, find_droplets, find_snapshots

user_config_file = Path(user_config_dir(appname="DOGS", roaming=True, appauthor=False), "config.yaml")
local_config_file = Path("config.yaml")
if user_config_file.exists() and local_config_file.exists():
    print("Config files were found in both local and user directory, which do you want to use?")
    opts = [user_config_file, local_config_file]
    config_file = opts[cutie.select(opts)]
elif user_config_file.exists():
    print("Using stored config file")
    config_file = user_config_file
elif local_config_file.exists():
    print("Using local config file")
    config_file = local_config_file
else:
    # TODO
    raise Exception("No config file found!")

config = Box.from_yaml(filename=config_file)


def stats(server):
    print(f"\nServer: {server}\n")
    tabbed = "\n    "
    drops = find_droplets(server, config)
    if drops:
        print(" Droplets:")
        print(f"    {tabbed.join(drops)}")
    snaps = find_snapshots(server, config)
    if snaps:
        print(" Snapshots:")
        print(f"    {tabbed.join(snaps)}")
    return True if drops and len(drops) == 1 else False


for i in count():
    print("\nWhich server do you want to manage?")
    opts = list(config.servers) + ['Exit']
    selection = cutie.select(options=opts)
    if selection == len(opts) - 1:
        break
    server_name = list(config.servers)[selection]
    online = stats(server_name)

    print("\nManage:")
    actions = [
        "Turn On",
        "Shutdown",
        "Cleanup Old Snapshots",
        "Cancel"
    ]
    action = actions[cutie.select(actions)]
    dogs = DOGS(server_name, config_file)
    if action == "Turn On":
        print("\nTurning droplet on\n")
        dogs.create()
    elif action == "Shutdown":
        print("\nShutting down droplet\n")
        dogs.destroy()
    elif action == "Cleanup Old Snapshots":
        print("\nRemoving old snapshots\n")
        dogs.cleanup()



