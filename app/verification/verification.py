"""
Handle checking if the minting address is allowed to mint.
"""

import os
from web3 import Web3

VERIFICATION_RPC_URL = os.environ["VERIFICATION_RPC_URL"]
VERIFICATION_CONTRACT_ADDRESS = os.environ["VERIFICATION_CONTRACT_ADDRESS"]
VERIFICATION_CONTRACT_ABI = [
    {
        "type": "function",
        "stateMutability": "view",
        "outputs": [{"type": "bool", "name": "", "internalType": "bool"}],
        "name": "isVerifiedUser",
        "inputs": [{"type": "address", "name": "_user", "internalType": "address"}],
    },
]


def is_verified(address: str) -> bool:
    """
    Check if the address is verified.
    """

    if Web3.isAddress(address) is False:
        raise Exception("Verification address is not a valid address")

    if VERIFICATION_RPC_URL == "" or VERIFICATION_CONTRACT_ADDRESS == "":
        return True

    web3 = Web3(Web3.WebsocketProvider(VERIFICATION_RPC_URL))

    contract = web3.eth.contract(
        address=Web3.toChecksumAddress(VERIFICATION_CONTRACT_ADDRESS),
        abi=VERIFICATION_CONTRACT_ABI,
    )

    is_verified_user: bool = contract.functions.isVerifiedUser(address).call()

    return is_verified_user is True
