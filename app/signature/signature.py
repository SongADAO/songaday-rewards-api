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

    # TODO: Verify signature
    is_valid: bool = True

    return is_valid is True
