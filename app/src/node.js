const Web3 = require("web3");

const fs = require("fs");
const URLProvider = "http://localhost:8546";
const Contract = require("web3-eth-contract");

class Node {
    // let contract;
    constructor() {
        this.contract = null;
    }

    connectToContract = async function() {
        if (this.contract != null) return;
        var web3 = new Web3(Web3.givenProvider || URLProvider);

        console.log("connecting..");
        if (await web3.eth.net.isListening()) {
            console.log("is connected");
        } else {
            console.log("Wow. Something went wrong: ");
        }
        Contract.setProvider(URLProvider);
        let contractjson = (await fetch('abi.json')).json;
        let contractAddress = (await fetch('contract-address.txt')).text;

        this.contract = new Contract(abi, contractAddress);
    };

    getState = async function() {
        return await this.contract.methods.getState().call();
    };
}

let some = async function() {

    let node = new Node();

    await node.connectToContract();
}

some()

export default Node;