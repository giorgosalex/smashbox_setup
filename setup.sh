#!/bin/bash

if [[ $# -ne 8 ]]; then
    echo "You must give exactly 8 arguments. Use: ./setup.sh -v VERSION -u USERNAME -p PASSWORD -k KIBANA_ACTIVITY"
    exit
fi

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -v|--version) #owncloud client version
    VERSION="$2"
    shift # past argument
    shift # past value
    ;;
    -u|--username) #owncloud client account name
    USERNAME="$2"
    shift
    shift
    ;;
    -p|--password) #owncloud client account password
    PASSWORD="$2"
    shift
    shift
    ;;
    -k|--kibana_activity) #kibana activity
    K_ACTIVITY="$2"
    shift
    shift
    ;;
    *)    # unknown option
    echo $1 ": no such option"
    exit
    ;;
esac
done

echo $VERSION
echo $USERNAME
echo $PASSWORD
echo $K_ACTIVITY
#exit

#vers=$(python get_vers.py)
vers=$(python get_vers.py -v $VERSION)
echo $vers

if [[ $? != 0 ]]; then
    echo "failed: $vers" 
    exit
fi

#yum install wget -y
#yum install git -y

wget http://cernbox.cern.ch/cernbox/doc/Linux/centos7-cernbox.repo
mv centos7-cernbox.repo /etc/yum.repos.d/cernbox.repo

sed -i s+/repo/+/$vers/+g /etc/yum.repos.d/cernbox.repo

#yum update -y
#yum install cernbox-client -y

rm /etc/yum.repos.d/cernbox.repo

git clone https://github.com/cernbox/smashbox.git /root/smashbox/

CURRENT_PATH=$(pwd)
cp $CURRENT_PATH/auto-smashbox.conf /root/smashbox/etc/smashbox-cernbox.conf

echo "oc_account_name = '$USERNAME'" >> /root/smashbox/etc/smashbox-cernbox.conf
echo "oc_account_password = '$PASSWORD'" >> /root/smashbox/etc/smashbox-cernbox.conf
echo "oc_ssl_enabled = True" >> /root/smashbox/etc/smashbox-cernbox.conf
echo 'oc_sync_cmd = "/usr/bin/cernboxcmd --trust"' >> /root/smashbox/etc/smashbox-cernbox.conf
echo 'kibana_activity = "'$K_ACTIVITY'"' >> /root/smashbox/etc/smashbox-cernbox.conf

cp /root/smashbox/etc/smashbox-cernbox.conf /root/smashbox/etc/smashbox-testbox.conf
echo 'oc_server = "cernbox.cern.ch/cernbox/desktop"' >> /root/smashbox/etc/smashbox-cernbox.conf
echo 'oc_server = "cernbox.cern.ch/testbox/desktop"' >> /root/smashbox/etc/smashbox-testbox.conf
touch /root/smashbox/etc/smashbox.conf

crontab -l > mycron
echo "00 20 * * * python /root/smashbox/bin/smash --keep-going -a -d /root/smashbox/lib/test_* -c /root/smashbox/etc/smashbox-cernbox.conf" >> mycron
echo "00 23 * * * python /root/smashbox/bin/smash --keep-going -a -d /root/smashbox/lib/test_* -c /root/smashbox/etc/smashbox-testbox.conf" >> mycron
crontab mycron
rm mycron

