import sys
from node import Node
from constants import *


if __name__ == "__main__":
    nodeId = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    gethHttp = f"http://localhost:{8545 + nodeId}"

    node = Node(gethHttp)

    contractAdd = node.executeSmartContractFromFile(SMART_CONTRACT_FILE, ABI_FILE)

    open(CONTRACT_ADDRESS_FILE, 'w').write(str(contractAdd))

    print(f"Wrote contract address to {CONTRACT_ADDRESS_FILE } file")
