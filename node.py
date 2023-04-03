import os
import pickle
# from multilayerPerceptron import MultilayerPerceptronLearner
from learning import Learner
from solcx import compile_source
from web3 import Web3
from web3.contract.contract import Contract
from web3.types import TxParams
import numpy as np
import time
from constants import *
import json
from pprint import pprint


transaction_parameters = TxParams({ 'gas': GAS_LIMIT }) #type: ignore


class Node:
    def __init__(self, gethHttp: str, datasetFile: str) -> None:
        self.w3 = self.connectNode(gethHttp)
        self.contract = None
        self.learner = Learner(datasetFile)

    def connectNode(self, gethHttp: str):
        del os.environ['http_proxy']
        del os.environ['https_proxy']

        w3 = Web3(Web3.HTTPProvider(gethHttp))
        assert(w3.is_connected())
        w3.eth.default_account = w3.eth.accounts[0]
        # w3.personal.unlockAccount(w3.personal.listAccounts[0], "password")

        return w3

    def executeSmartContractFromFile(self, smartContractFile: str, abiFile: str):
        # Owner node
        abi, bytecode = self.comipleContract(smartContractFile)
        with open(abiFile, 'w') as f:
            json.dump(abi, f)
        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = Contract.constructor(
            initialWeights=self.getModelBytes()).transact(transaction_parameters)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt.status, tx_receipt.contractAddress  # type: ignore

    def getModelBytes(self):
        # print(self.learner.getModel())
        return pickle.dumps(self.learner.getModel())

    @staticmethod
    def comipleContract(smartContractFile: str):
        assert(os.path.isfile(smartContractFile))

        compiled_sol = compile_source(
            open(smartContractFile, 'r').read(), output_values=['abi', 'bin'])

        _, contract_interface = compiled_sol.popitem()
        bytecode = contract_interface['bin']
        abi = contract_interface['abi']

        return abi, bytecode

    def connectSmartContract(self, contractAdd: str, abiFile: str):
        self.contractAdd = contractAdd

        with open(abiFile, 'r') as f:
            abi = json.load(f)

        self.contract = self.w3.eth.contract(
            address=contractAdd, abi=abi  # type: ignore
        )

    #return state, roundNo, roundEnd
    def getState(self):
        return self.contract.functions.getState().call(transaction_parameters)

    def getGlobalModel(self):
        assert(isinstance(self.contract, Contract))

        roundNo, raw_models = self.contract.functions.getGlobalModel().call(
            transaction_parameters)
        # raw_models = [( bytes weights, uint256 score )]

        coefficients, intercepts, scores = [], [], []
        for _, weights, score, _ in raw_models:
            coef, intercept = pickle.loads(weights)
            coefficients.append(coef)
            intercepts.append(intercept)
            scores.append(score)

        print(scores)

        coefAvg = np.average(coefficients, weights=scores, axis=0)
        interceptAvg = np.average(intercepts, weights=scores, axis=0)

        # print(coefAvg, interceptAvg)
        return coefAvg, interceptAvg

    def train(self):
        self.learner.train()
        print(f"Finished Training Model, score: ", self.learner.score())

    def sendModel(self):
        assert(isinstance(self.contract, Contract))
        self.waitTill(POLLING)

        self.makeTransaction(
            self.contract.functions.sendModel(self.getModelBytes()))
        print("Send Model Successfull")

    def makeTransaction(self, transaction):
        txnHash = transaction.transact(transaction_parameters)
        txnReceipt = self.w3.eth.wait_for_transaction_receipt(txnHash)
        assert(txnReceipt["status"] == 1)

    def validateModels(self):
        assert(isinstance(self.contract, Contract))
        self.waitTill(VALIDATING)

        # [(address, weights)]
        validationModels = self.contract.functions.getValidationModels().call(
            transaction_parameters)
        # print(validationModels)

        modelScores = []

        for address, weights, _, _ in validationModels:
            modelScores.append(
                (address, int(SCORE_SCALE_FACTOR * self.learner.validateModel(pickle.loads(weights)))))

        print(modelScores)

        self.waitTill(VALIDATING)
        self.makeTransaction(self.contract.functions.sendValidation(
            modelScores))

        print("Validation Successfull")

    def updateModel(self):
        self.learner.model = self.learner.makeModel(self.getGlobalModel()) #type: ignore
        print(f"Updated Model to global Model, score: ", self.learner.score())

    def updateState(self):
        assert(isinstance(self.contract, Contract))
        self.makeTransaction(self.contract.functions.setState())

    def waitTill(self, targetState):
        assert(isinstance(self.contract, Contract))
        state, _, roundEnd = self.contract.functions.getState().call(transaction_parameters)
        now = int(time.time())
        # print(now - roundEnd)
        # print(f"{state=} {roundEnd=} {now=}")

        if now >= roundEnd:
            state = int(not state)

        if state != targetState:
            timeLeft = roundEnd - now + TIME_MARGIN
            if timeLeft > 0:
                print(f"Waiting {timeLeft} seconds till {'validation' if targetState == 1 else 'polling'}")
                time.sleep(timeLeft)
            else:
                self.updateState()
                self.waitTill(targetState)
    
