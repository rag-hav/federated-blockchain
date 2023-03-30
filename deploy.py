import sys
from node import Node
from constants import *


if __name__ == "__main__":
    nodeId = len(sys.argv) > 1 and int(sys.argv[1]) or 1
    gethHttp = f"http://localhost:{8545 + int(nodeId)}"
    datasetFile = f"dataset/iot23_{str( nodeId ).zfill(2)}.csv"

    node = Node(gethHttp, datasetFile)

    contractAdd = node.executeSmartContractFromFile(SMART_CONTRACT_FILE)
    open(CONTRACT_ADDRESS_FILE, 'w').write(str(contractAdd))

    print(f"Wrote contract address to {CONTRACT_ADDRESS_FILE } file")
