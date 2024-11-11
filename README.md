# Initialize

## Installing Dependencies
```
sudo pip install -r requirement.txt
```
_if error, can use this command_
```
sudo pip3 install -r requirement.txt
```

## Change the following data

```
nano alert_discord.py
```
```
---
token = "TOKEN_DISCORD_APPS"

container_channel_ID    = "CHANNEL_ID_CONTAINER"
node_channel_ID         = "CHANNEL_ID_NODE"
traffic_channel_ID      = "CHANNEL_ID_TRAFFIC"
nginx_channel_ID        = "CHANNEL_ID_NGINX"
apache_channel_ID       = "CHANNEL_ID_APACHE"
---
```

## Setup for Script Python

Setup for the service that runs this python program in the backgroud
```
sudo cp alert_discord.service /etc/systemd/system/
sudo cp alert_discord.py /usr/local/bin/
```
```
sudo systemctl daemon-reload
sudo systemctl start alert_discord.service
sudo systemctl status alert_discord.service
```
