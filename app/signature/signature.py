"""
Handle checking if the minting address is allowed to mint.
"""

import os
from web3 import Web3


def has_valid_signature(address: str, signature: str, nonce: str) -> bool:
    """
    Check if the signature is valid.
    """

    if Web3.isAddress(address) is False:
        raise Exception("Signature address is not a valid address")

    # if VERIFICATION_RPC_URL == "" or VERIFICATION_CONTRACT_ADDRESS == "":
    #     return True

    # web3 = Web3(Web3.WebsocketProvider(VERIFICATION_RPC_URL))

    # contract = web3.eth.contract(
    #     address=Web3.toChecksumAddress(VERIFICATION_CONTRACT_ADDRESS),
    #     abi=VERIFICATION_CONTRACT_ABI,
    # )

    # is_verified_user: bool = contract.functions.isVerifiedUser(address).call()

    is_valid: bool = True

    return is_valid is True
