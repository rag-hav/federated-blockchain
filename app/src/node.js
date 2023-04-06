const Web3 = require("web3");

const URLProvider = "http://localhost:8546";
const Contract = require("web3-eth-contract");

class Node {
  // let contract;
  constructor() {
    this.contract = null;
  }

  connectToContract = async function () {
    if (this.contract != null) return;
    var web3 = new Web3(Web3.givenProvider || URLProvider);

    if (await web3.eth.net.isListening()) {
      console.log("Connected to Node");
    } else {
      console.log("Wow. Something went wrong: ");
    }
    Contract.setProvider(URLProvider);
    let abi = await (await fetch("abi.json")).json();
    let contractAddress = await (await fetch("contract-address.txt")).text();

    // console.log(abi);
    // console.log(contractAddress);

    this.contract = new Contract(abi, contractAddress);
  };

  getState = async function () {
    try {
      return await this.contract.methods.getState().call();
    } catch (e) {
      console.log(e);
      return [];
    }
  };
  getRoundDetails = async function () {
    try {
      return await this.contract.methods.getRoundDetails(15).call();
    } catch (e) {
      console.log(e);
      return [];
    }
  };
}

export { Node };