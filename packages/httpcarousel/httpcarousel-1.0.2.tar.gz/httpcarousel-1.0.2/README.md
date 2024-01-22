# Carousel

Serve images via HTML / JavaScript which rotate every N seconds.

## Installation

Via Pipx:

`pipx install httpcarousel`

Sample systemd unit:

```shell
sudo tee -a /etc/systemd/system/httpcarousel.service > /dev/null <<EOF
[Unit]
Description=httpcarousel
After=network.target

[Service]
Type=notify
User=debian
Group=debian
ExecStart=/home/debian/.local/pipx/venvs/httpcarousel/bin/carousel
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target

EOF

sudo systemctl daemon-reload
sudo systemctl start httpcarousel
sudo systemctl enable httpcarousel
```

## Environment Variables

| Name | Description | Default |
| ---- | ----------- | ------- |
| CAROUSEL_PORT | The HTTP Port that Carousel should listen on | `6502` |
| CAROUSEL_INTERVAL | How often the displayed image should change in seconds | `45` |
| CAROUSEL_IMAGE_DIRECTORY | The directory to find images | `/tmp/images` |
