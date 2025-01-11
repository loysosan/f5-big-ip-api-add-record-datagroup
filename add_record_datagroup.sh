#!/bin/bash

F5_URL="https://f5-big-ip.yourloadbalancer.com/mgmt/tm/ltm/data-group/internal/NameYourDatagroup" # 
USERNAME=""  # Replace with your username
PASSWORD=""  # Replace with your password

add_record() {
    local ip="$1"
    local value="$2"
    local curl_command="curl -X PATCH -H 'Content-Type: application/json' -d '{\"name\":\"NameYourDatagrou\"}' -ku \"$USERNAME:$PASSWORD\" \"$F5_URL?options=records%20add%20%7b%20$ip%20%7b%20data%20$value%20%7d%20%7d\""
    eval "$curl_command"
    echo "Record $ip:$value added"
}

delete_record() {
    local ip="$1"
    local curl_command="curl -X PATCH -H 'Content-Type: application/json' -d '{\"name\":\"NameYourDatagrou\"}' -ku \"$USERNAME:$PASSWORD\" \"$F5_URL?options=records%20delete%20%7b%20$ip%20%7d\""
    eval "$curl_command"
    echo "Record $ip deleted"
}

if [ "$1" == "add" ]; then
    if [ -z "$2" ] || [ -z "$3" ]; then
        echo "Usage: $0 add <IP-address> <Value>"
        exit 1
    fi
    add_record "$2" "$3"
elif [ "$1" == "del" ]; then
    if [ -z "$2" ]; then
        echo "Usage: $0 del <IP-address>"
        exit 1
    fi
    delete_record "$2"
else
    echo "Usage: $0 {add|del} <IP-address> [Value]"
    exit 1
fi