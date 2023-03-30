import os
import pickle
from eth_typing import Address
from learning import Learner
from solcx import compile_source
from web3 import Web3
from web3.contract.contract import Contract
import numpy as np
import time
from constants import *


class Node:
    def __init__(self, gethHttp, datasetFile) -> None:
        self.connectNode(gethHttp)
        self.learner = Learner(datasetFile)

    def connectNode(self, gethHttp):
        del os.environ['http_proxy']
        del os.environ['https_proxy']

        self.w3 = Web3(Web3.HTTPProvider(gethHttp))
        assert(self.w3.is_connected())
        self.w3.eth.default_account = self.w3.eth.accounts[0]

    def executeSmartContractFromFile(self, smartContractFile: str):
        # Owner node
        abi, bytecode = self.comipleContract(smartContractFile)
        from json import dumps
        open('abi.json', 'w').write(dumps(abi))
        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = Contract.constructor(
            initialWeights=self.getModelBytes()).transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt.contractAddress  # type: ignore

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

    def connectSmartContract(self, contractAdd: str, smartContractFile: str):
        self.contractAdd = contractAdd
        abi, _ = self.comipleContract(smartContractFile)

        self.contract = self.w3.eth.contract(
            address=contractAdd, abi=abi  # type: ignore
        )

    def getGlobalModel(self):
        assert(isinstance(self.contract, Contract))

        roundNo, raw_models = self.contract.functions.getGlobalModel().call()
        # raw_models = [( bytes weights, uint256 score )]

        coefficients, intercepts, scores = [], [], []
        for _, weights, score, _ in raw_models:
            coef, intercept = pickle.loads(weights)
            coefficients.append(coef)
            intercepts.append(intercept)
            scores.append(score)

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

        status = self.contract.functions.sendModel(
            self.getModelBytes()).transact()
        print(f"Send Model {status and 'successful' or 'failed'}")

    def validateModels(self):
        assert(isinstance(self.contract, Contract))
        self.waitTill(VALIDATING)

        # [(address, weights)]
        validationModels = self.contract.functions.getValidationModels().call()
        print(validationModels)

        modelScores = []

        for address, weights, _, _ in validationModels:
            modelScores.append(
                (address, int(self.learner.scoreModel(pickle.loads(weights)))))

        self.waitTill(VALIDATING)
        status = self.contract.functions.sendValidation(modelScores).transact()
        print(f"Validate Models {status and 'successful' or 'failed'}")

    def updateModel(self):
        self.learner.model = self.learner.makeModel(self.getGlobalModel())
        print(f"Updated Model to global Model, score: ", self.learner.score())

    def waitTill(self, phase):
        assert(isinstance(self.contract, Contract))
        curPhase = self.contract.functions.state().call()

        if curPhase != phase:
            roundStart = self.contract.functions.roundStart().call()
            timeLeft = roundStart + \
                (curPhase == POLLING and POLLING_TIME or VALIDATION_TIME) - \
                time.time() + TIME_MARGIN
            if timeLeft > 0:
                time.sleep(timeLeft)
