#!/bin/bash


num=$1
id=miner$num
dir=$(pwd)/$id

rm $dir -rf
mkdir $dir

geth --datadir $dir init genesis.json
geth --datadir $dir account new

echo "password" > $dir/password.sec
