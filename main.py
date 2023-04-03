import sys
from node import Node
from constants import *

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

    _, round, _ = node.getState()
    while True:
        print("Starting round", round)
        node.train()
        node.sendModel()
        node.validateModels()
        node.updateModel()
        round += 1
