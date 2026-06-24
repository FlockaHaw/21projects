#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo ">> Root required!" >&2
    exit 1
fi

echo "\n>> Deleting users..."
userdel -r user 2>/dev/null
userdel -r secret_agent 2>/dev/null
userdel -r secret_spy 2>/dev/null
userdel -r secret_boss 2>/dev/null
echo ">> OK"

echo "\n>> Deleting groups..."
groupdel default_users 2>/dev/null
groupdel secret_users 2>/dev/null
echo ">> OK"

echo "\n>> Setting default perms to 'var'..."
chmod 755 /var
echo ">> Dir '/var' got default settings (755)."

echo "\n>> Setting passwd req to default group..."
sed -i '/%default_users ALL=(ALL) NOPASSWD: ALL/d' /etc/sudoers
echo ">> OK"

echo "\n>> Deleting apach2 packages..."
if dpkg -l | grep apache2; then
    apt-get remove -y apache2*
fi
echo "\n>> Apache2 packages were deleted."

echo -e "\n>> All existing user:"
getent passwd | awk -F: '{if ($3 >= 1000 && $3 < 65534) print $1}' | sort

echo -e "\n>> All changes been cancelled !"
