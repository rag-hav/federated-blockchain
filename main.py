import sys
from node import Node
from constants import *
from time import sleep, time

if __name__ == "__main__":
    assert(len(sys.argv) > 1)
    nodeId = int(sys.argv[1])
    gethHttp = f"http://localhost:{8545 + int(nodeId)}"
    datasetFile = f"dataset/iot23_{str( nodeId ).zfill(2)}.csv"

    node = Node(gethHttp, datasetFile)
    contractAdd = open(CONTRACT_ADDRESS_FILE, 'r').read()
    print("Read Contract Address from", CONTRACT_ADDRESS_FILE)

    node.connectSmartContract(contractAdd, ABI_FILE)
    print("Connected to node", nodeId)

    while True:
        node.updateState()

        print(
            f"\nRound Number {node.roundNo} in state {node.state and 'VALIDATING' or 'POLLING'}")
        startTime = time()
        endTime = 0
        if node.state == POLLING:
            node.train()
            try:
                node.sendModel()
                endTime = time()
                node.waitTill(VALIDATING)
            except Exception as e:
                print("Send Models failed!")
                print(e)

        else:
            node.validateModels()
            # State might have changed during training
            try:
                node.sendValidations()
                endTime = time()
                node.waitTill(POLLING)
            except Exception as e:
                print("Send Validations failed!")
                print(e)
        print(f"timetaken {startTime - endTime}")
