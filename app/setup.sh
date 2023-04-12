#!/bin/bash

cp ../contract-address.txt public/contract-address.txt 
cp ../abi.json public/abi.json 


num=$1
http_port=8545
let "http_port+=num"

cat <<EOF > src/constants.js
// This file is generated using setup.sh
const URLProvider = "http://localhost:${http_port}";
export {URLProvider};
EOF
