#!/bin/bash

if [ "$(id -u)" != "0" ]; then
	echo "Root permissions required!" >&2
	exit 1
fi

INFO_FILE="info"
rm -f "$INFO_FILE"

echo "Checking installed packages..."
echo ">>>>>> Installed packages (dpkg/rpm)<<<<<<" >> "$INFO_FILE"
if command -v dpkg >/dev/null 2>&1; then
	dpkg -l >> "$INFO_FILE"
elif command -v rpm >/dev/null 2>&1; then
	rpm -qa >> "$INFO_FILE"
else
	echo "Unknown file manager: dpkg/rpm not found." >> "$INFO_FILE"
fi

echo "" >> "$INFO_FILE"

echo "Checking current processes..."
echo ">>>>>> Current processes (ps aux) <<<<<<" >> "$INFO_FILE"
ps aux >> "$INFO_FILE"

echo "Checking all open ports..."
echo ">>>>>> All open ports (netstat) <<<<<<" >> "$INFO_FILE"
if command -v netstat >/dev/null 2>&1; then
	netstat -tun >> "$INFO_FILE"
else
	echo "Netstat not found."
fi

echo "" >> "$INFO_FILE"

echo "Installing 'CowSay' and 'sl'..."
echo ">>>>>> Installing 'CowSay' and 'sl' <<<<<<" >> "$INFO_FILE"
if command -v apt-get >/dev/null 2>&1; then
	apt-get install -y cowsay sl >> "$INFO_FILE" 2>&1
elif command -v yum >/dev/null 2>&1; then
	yum  install -y cowsay sl >> "$INFO_FILE" 2>&1
elif command -v dnf >/dev/null 2>&1; then
	dnf install -y cowsay sl >> "$INFO_FILE" 2>&1
else
	echo "Unknown package manager. Unavaliable to install packages."
fi

echo "" >> "$INFO_FILE"

echo "Collecting system info..."
echo ">>>>>> System info  <<<<<<" >> "$INFO_FILE"
uname -a >> "$INFO_FILE"
echo "" >> "$INFO_FILE"

if [ -f /etc/os-release ]; then
	cat /etc/os-release >> "$INFO_FILE"
else
	echo "Sys info couldnt be found."
fi

echo "" >> "$INFO_FILE"

tar -cf OS_RESULT.tar "$INFO_FILE"

rm -f "$INFO_FILE"

echo "Information collected and wrote on arcive OS_RESULT.tar"
