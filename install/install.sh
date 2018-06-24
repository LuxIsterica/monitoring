#!/bin/bash

GREEN='\e[32m'
RED='\e[31m'
NOCOL='\033[0m'

ok() {
echo -e "${GREEN}
$1
${NOCOL}"
sleep 1
}

err() {
echo -e "${RED}
$1
${NOCOL}"
}



ok "Adding mongo GPG key..."
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
ret=$?
test $ret -ne 0 && err "error during mongo gog key add" && exit $ret

ok "Adding mongo 3.6 repository..."
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" > /etc/apt/sources.list.d/mongodb-org-3.6.list

ok "Reloading apt packages cache..."
sudo apt-get update

ok "python3, python3-pip and MongoDB 3.6 installation..."
sudo apt-get install -y python3 python3-pip mongodb-org

ok "Starting mongodb service..."
sudo systemctl start mongod
ret=$?
test $ret -ne 0 && err "error during mongodb service start" && exit $ret

mongofile="dbuser.js"
ok "Creating nomodo mongo user..."
read -p "Enter a password for mongo 'nomodo' user: " nomodopass
echo "db.createUser({user: 'nomodo', pwd: '$nomodopass', roles: ['root'] })" > $mongofile
mongo admin $mongofile
rm -f $mongofile

ok "Installing python3 requirements..."
if [ -f requirements.txt ]
then
	pip3 install -r requirements.txt
else
	err "File requirements.txt not found"
	exit 1
fi
