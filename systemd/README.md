## Systemd Service Configuration

```shell
sudo cp leniac-client.service /etc/systemd/system/
sudo cp leniac-server.service /etc/systemd/system/

# To grante permissions and privileges:
sudo chown mokira3d48:mokira3d48 /home/mokira3d48/leniac-server
sudo chown obrymec:obrymec /home/obrymec/leniac-client

# To apply configurations and start services:
sudo systemctl daemon-reload
sudo systemctl start leniac-client.service
sudo systemctl start leniac-server.service
sudo systemctl status leniac-client.service
sudo systemctl status leniac-server.service

# To show logging in real time:
sudo journalctl -u leniac-client.service -f
sudo journalctl -u leniac-server.service -f
```
