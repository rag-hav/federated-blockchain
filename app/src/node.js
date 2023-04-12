import { URLProvider } from "./constants.js";

const Contract = require("web3-eth-contract");
const Web3 = require("web3");

class Node {
  // let contract;
  constructor() {
    this.contract = null;
    this.isReady = this._connectToContract();
  }



  _connectToContract = async function () {
    if (this.contract != null) return;

    var web3 = new Web3(Web3.givenProvider || URLProvider);

    if (await web3.eth.net.isListening()) {
      console.log("Connected to Node");
    } else {
      console.log("Wow. Something went wrong: ");
    }
    console.log("trying jor se");

    Contract.setProvider(URLProvider);
    let abi = await (await fetch("abi.json")).json();
    let contractAddress = await (await fetch("contract-address.txt")).text();

    this.contract = new Contract(abi, contractAddress);
  };

  getState = async function () {
    try {
      await this.isReady;
      return await this.contract.methods.getState().call();
    } catch (e) {
      console.log(e);
      return [];
    }
  };
  getRoundDetails = async function () {
    try {
      await this.isReady;
      return await this.contract.methods.getRoundDetails(15).call();
    } catch (e) {
      console.log(e);
      return [];
    }
  };
}

export { Node };
