#!/bin/bash

num=$1
dir=$(pwd)/miner$num


id=miner$num
port=30302
http_port=8545

let "port+=num"
let "http_port+=num"

echo "Starting ethereum node from directory: ${dir} with name ${id} on port ${port} and http_port ${http_port}"

geth --dev --identity $id --networkid 42 --datadir $dir \
    --nodiscover --allow-insecure-unlock --mine --http --port $port --http.corsdomain "*" \
    --http.port $http_port --unlock 0 \
    --password $dir/password.sec --ipcpath $dir/ipc
