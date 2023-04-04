var Web3 = require('web3');
const fs = require('fs');
const URLProvider = 'http://localhost:8546';
var Contract = require('web3-eth-contract');

// set provider for all later instances to use
class Node


async function connectToContract() {
    var web3 = new Web3(Web3.givenProvider || URLProvider);
    console.log('connecting..')
    if (await web3.eth.net.isListening()) {
        console.log('is connected')
    } else {
        console.log('Wow. Something went wrong: ' + e);
    }
    Contract.setProvider(URLProvider);
    var contractjson = fs.readFileSync('/home/akanksha/projects/federated-blockchain/abi.json');
    var abi = JSON.parse(contractjson);
    var contractAddress = fs.readFileSync('/home/akanksha/projects/federated-blockchain/contract-address.txt').toString();
    var contract = new Contract(abi, contractAddress);
    // console.log(await contract.methods.getState().call());
    return contract;
}



connectToContract();