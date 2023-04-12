#!/bin/bash


num=$1
id=miner$num
dir=$(pwd)/$id
password=""
static=$(pwd)/static-nodes.json

rm $dir -rf
mkdir $dir

echo "Use '$password' as password\n"
geth --datadir $dir init genesis.json
geth --datadir $dir account new

echo $password > $dir/password.sec

echo "[]" > $static
ln -s $static $dir/static-nodes.json
