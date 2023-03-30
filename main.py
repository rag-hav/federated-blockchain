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
    print("Read Contract Address")

    node.connectSmartContract(contractAdd, SMART_CONTRACT_FILE)
    print("Connected to node", nodeId)

    round = 1
    while True:
        print("Starting round", round)
        node.train()
        node.sendModel()
        node.validateModels()
        node.updateModel()
        round += 1
