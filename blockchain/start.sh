#!/bin/bash

proxy=$http_proxy
unset http_proxy https_proxy

num=$1
id=miner$num
dir=$(pwd)/$id


port=30302
http_port=8545
authrpc_port=8550

let "port+=num"
let "http_port+=num"
let "authrpc_port+=num"

echo "Starting ethereum node from directory: ${dir} with name ${id} on port ${port} and http_port ${http_port}"

geth --identity $id --networkid 42 --datadir $dir \
    --nodiscover --allow-insecure-unlock --mine --http --port $port --http.corsdomain "*" \
    --http.port $http_port --unlock 0 \
    --authrpc.port $authrpc_port \
    --password $dir/password.sec --ipcpath $dir/ipc &>$id.log &


sleep 5s
geth --preload preload.js attach $dir/ipc

wait

export http_proxy=$proxy
export https_proxy=$proxy
