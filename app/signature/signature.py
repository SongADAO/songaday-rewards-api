"""
Handle checking if the minting address is allowed to mint.
"""

from web3 import Web3
from eth_account.messages import defunct_hash_message
from .config import (
    SIGNATURE_MESSAGE,
)


def has_valid_signature(address: str, signature: str, nonce: str) -> bool:
    """
    Check if the signature is valid.
    """

    address = Web3.toChecksumAddress(address)

    web3 = Web3()

    if Web3.isAddress(address) is False:
        raise Exception("Signature address is not a valid address")

    original_message = SIGNATURE_MESSAGE + nonce
    message_hash = defunct_hash_message(text=original_message)

    signer: str = web3.eth.account.recoverHash(message_hash, signature=signature)

    return Web3.toChecksumAddress(address) == Web3.toChecksumAddress(signer)
