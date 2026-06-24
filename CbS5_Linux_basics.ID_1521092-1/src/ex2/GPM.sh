#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo "Root required!!" >&2
    exit 1
fi

groupadd default_users
useradd -m -G default_users user
echo ">> Created user 'user' and group 'default_users.'"

groupadd secret_users
useradd -m -G secret_users secret_agent
useradd -m -G secret_users secret_spy
useradd -m -G secret_users secret_boss
echo ">> Created secret_agent, secret_spy, secret_boss in secret_users group."

chmod 750 /home/secret_agent
chmod 750 /home/secret_spy
chmod 750 /home/secret_boss
chown :secret_users /home/secret_agent /home/secret_spy /home/secret_boss
echo ">> Setuped access policy fro each home dirs."

chmod 777 /var
echo ">> Dir '/var' is availible for every users now."

apt-get update
apt-get install -y apache2
systemctl status apache2 --no-pager
echo ">> Installed apache2"
echo "%default_users ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
echo ">> All users from default_users group now can use sudo without password."

