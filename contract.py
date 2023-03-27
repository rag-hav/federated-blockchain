import os
from solcx import compile_source
from web3 import Web3
from pprint import pprint

smartContractFile = "federated-learning.sol"
gethHttp = 'http://localhost:8546'

assert(os.path.isfile(smartContractFile))

compiled_sol = compile_source(open(smartContractFile, 'r').read(), output_values = ['abi', 'bin'])

contract_id, contract_interface = compiled_sol.popitem()
bytecode = contract_interface['bin']
abi = contract_interface['abi']

w3 = Web3(Web3.HTTPProvider(gethHttp))

assert(w3.is_connected())

pprint(abi)
