# DOGS - Digital Ocean Gaming Services

On demand gaming server for pennies a month!

## TLDR;

Game hosting isn't too expensive, but if you're only playing a few nights a
month, you can save money if you're a bit technical. This script helps make the
process easier.

## Usage

```sh
git clone https://github.com/OneHoopyFrood/dogs.git
# Alternatively, just download and extract the zip file
# https://github.com/cdgriffith/dogs/archive/master.zip

# Create a venv if you are python savvy
pip install requirements.txt
cp config.yaml.example config.yaml
# Update the config file to match your digital ocean settings
python -m dogs
```

### Prerequisites

1. A Digital Ocean account token
2. A pre-established droplet (See below)

- You will need the hostname for this droplet, so make a note of it.

3. Your SSH key id, which are the digits at the very end of the public key.

- For example if the key ends with rsa-key-20190721 the ssh id is 20190721.
- You can always find this information in the Accounts > Security section by
  selecting one of the keys and hitting “Edit”.

4. If you hook a firewall up to the droplet you will also need that ID, which
   can you retrieve via the API.

### Droplet setup

Right now you have to pre-establish a droplet before you can manage it via DOGS.
(PR's are welcome if you'd like to ease this for others.)

When you create the droplet, make sure to pick the smallest specs you think you
will need. You can always upgrade to _larger_ disk size, but **you cannot scale
back down later**.

### DOGS Server Config

When you got all the prerequisites, add them to the [config.yaml](config.yaml.example) file.

### _Binary (EXE) files_

If you want to package it into an easy to use exe (can also modify for mac or
linux binaries), just use the included build scripts.

```sh
# Windows specific requirements, otherwise just install 'pyinstaller'
pip install -r requirements-build.txt
python dogs\build.py
```

And now you should have a super handy dogs.exe in the dist directory. Don’t
forget to keep your config.yaml in the same directory as it!

# About DOGS:

Run short lived servers and save them as snapshots when done to save on $$$.

## Rationale

There are a great many services providing dedicated hosting for popular
collaborative games such as Minecraft, Factorio, Satisfactory, and the like. A
centrally hosted server allows players to come and go as they please and as
their schedules allow.

The only downside with most of these is _cost_. If you want your server to be up
24/7 and don't have (or just don't have the time) to manage the technical
details yourself, then these services are the way to go and pretty fair with
their prices, which typically range between $5~15 for small scale servers.

However, there is another niche that goes under-served. Those who play these
sorts of games with friends and family only upon occasion, never intending or
desiring to expand beyond this small community. If such a group hosts their game
server with one of the available services, the server will sit idle 90% of the
time, consuming resources for no purpose. Sure you can self host, but then
everyone is dependent on a single person to have it up and running and on the
power of that machine and the network it's hooked up to.

If you are technical and self-sufficient for setting up the gaming software,
and only play certain games intermittently, your costs can be significantly
reduced. By switching to using a Digital Ocean Droplet, you can pay only a few
dollars per month for an on-demand gaming server. Even if we played a few hours
every night after work and weekends, a droplet server may only be $1 or $2 a
month.

_Disclaimer: these numbers are based on rough estimations in March 2025_

## Ok... but why is this software necessary?

At this point you may be thinking “Oh! You just turn off the droplet when you’re
not using it!”, but alas, it is not that simple. Digital Ocean still charges for
servers even when powered off since they continue to hold onto reserved
resources. This appears to be standard business practice across all the hosting
giants. _(As of March 2025)_

The trick on how to save cash? When you’re not playing, turn the droplet off,
**then snapshot it and _destroy_ the droplet**. Then, when you want to play again,
restore the snapshot to a new droplet.

With the way Digital Ocean costs are structured, this incurs a much smaller cost
which depends only on the disk size of the snapshot.

**THE UPSHOT IS** that while this process is possible to do by hand, it's
painful. However, it's really very easy with a helper script, thus DOGS is born.
