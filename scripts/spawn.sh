#! /bin/bash

function rm-footprints {
    username=$1
    while true
        do
            rm -rf `find / -type f -user $username 2>/dev/null | grep -iv /proc`
            sleep 0.1
        done

    # if i can not cleanup your mess then you have no right to exist!
    exit -1
}

function spawn {
    username=$1
    client_binary_path=$2

    # create user
    useradd $username

    # create home-sh directory
    mkdir -p /root/isol/$username
    
    # run the client binary
    (cd /root/isol/$username && su -m $username -c $client_binary_path)
}



CLIENT_ID=$1
CLIENT_DIR="/etc/spawn"

username=`cat /proc/sys/kernel/random/uuid | tr -d -`
rm-footprints $username &    
spawn $username "${CLIENT_DIR}/${CLIENT_ID}"
