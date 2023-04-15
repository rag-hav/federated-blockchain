import os
from time import time, sleep
from multilayerPerceptron import MultilayerPerceptronLearner
from logistic import LogisticLearner
from solcx import compile_source
from web3 import Web3
from web3.contract.contract import Contract
from web3.types import TxParams
from constants import *
import json


transaction_parameters = TxParams({'gas': GAS_LIMIT})  # type: ignore


class Node:
    def __init__(self, gethHttp: str, datasetFile: str) -> None:
        self.w3 = self.connectNode(gethHttp)
        self.contract = None
        self.state, self.roundNo, self.roundEnd = -1, -1, -1
        # self.learner = LogisticLearner(datasetFile)
        self.learner = MultilayerPerceptronLearner(datasetFile)
        self.validationScores = []

    def connectNode(self, gethHttp: str):
        if 'http_proxy' in os.environ:
            del os.environ['http_proxy']
        if 'https_proxy' in os.environ:
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
            initialWeights=self.learner.getModelBytes()).transact(transaction_parameters)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt.status, tx_receipt.contractAddress  # type: ignore

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

        # Check Connection
        self.updateState()
        print("Successfully connected to contract")

    def getGlobalModel(self):
        assert(isinstance(self.contract, Contract))
        roundNo, raw_models = self.contract.functions.getGlobalModel().call(
            transaction_parameters)
        assert(roundNo == self.roundNo - 1)
        return raw_models

    def train(self):
        self.updateModel()
        self.learner.train()
        print(f"Finished Training Model, score: ", self.learner.score())

    def sendModel(self):
        assert(isinstance(self.contract, Contract))

        self.makeTransaction(
            self.contract.functions.sendModel(self.learner.getModelBytes()))
        print("Send Model Successfull")

    def makeTransaction(self, transaction):
        txnHash = transaction.transact(transaction_parameters)
        txnReceipt = self.w3.eth.wait_for_transaction_receipt(txnHash)
        assert(txnReceipt["status"] == 1)

    def validateModels(self):
        assert(isinstance(self.contract, Contract))

        # [(address, weights)]
        validationModels = self.contract.functions.getValidationModels().call(
            transaction_parameters)
        # print(validationModels)

        modelScores = []

        for address, weights, _, _ in validationModels:
            modelScores.append(
                (address, int(SCORE_SCALE_FACTOR * self.learner.scoreModel(weights))))

        self.validationScores = modelScores

    def sendValidations(self):
        assert(isinstance(self.contract, Contract))
        self.makeTransaction(self.contract.functions.sendValidation(
            self.validationScores, self.learner.datasetSize))

        print("Send Validation Successfull")

    def updateModel(self):
        self.learner.updateModel(self.getGlobalModel())
        print(f"Updated Model to global Model, score: ", self.learner.score())

    def updateState(self):
        assert(isinstance(self.contract, Contract))
        self.state, self.roundNo, self.roundEnd, self.stateLock = self.contract.functions.getState().call(
            transaction_parameters)

        if not self.stateLock and time() > self.roundEnd:
            # The round has ended
            self.stateLock = True
            self.state = int(not self.state)

    def waitTill(self, targetState):
        self.updateState()

        if (self.state != targetState):

            assert(not self.stateLock)
            timeLeft = 2 + self.roundEnd - int(time())
            print(f"Sleeping for {timeLeft}")
            sleep(timeLeft)

    # def hasAlreadyParticipated(self):
    #     assert(isinstance(self.contract, Contract))
    #     self.state, self.roundNo, roundEnd, stateLock = self.contract.functions.getState().call(
    #         transaction_parameters)

    #     if (self.state == POLLING):
    #         return
