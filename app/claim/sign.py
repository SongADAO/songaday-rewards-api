"""
Handle signing a metadata hash and trait hex for minting
"""

from eth_account import Account, messages
from eth_account.datastructures import SignedMessage
from web3 import Web3
from .config import (
    MINT_RPC_URL,
    MINT_CONTRACT_ADDRESS,
    MINT_SIGNER_PRIVATE_KEY,
)
from .abi import MINT_CONTRACT_ABI


def sign(
    approved_address: str,
    metadata_ipfs_hash_base16_bytes32: str,
    traits_bytes32: str,
) -> str:
    """
    Sign a metadata hash and trait hex for minting
    """

    web3 = Web3(Web3.HTTPProvider(MINT_RPC_URL))

    contract = web3.eth.contract(
        address=Web3.toChecksumAddress(MINT_CONTRACT_ADDRESS),
        abi=MINT_CONTRACT_ABI,
    )

    attribute_already_in_use: bool = contract.functions.tokenAttributeExists(
        traits_bytes32,
    ).call()

    if attribute_already_in_use is True:
        raise Exception("Attribute combination already in use")

    hash_to_sign: bytes = contract.functions.getTokenURIAndAttributeHash(
        approved_address,
        metadata_ipfs_hash_base16_bytes32,
        traits_bytes32,
    ).call()

    if not hash_to_sign:
        raise Exception("Could not get attribute hash to sign")

    # This part prepares "version E" messages, using the EIP-191 standard
    message_to_sign = messages.encode_defunct(primitive=hash_to_sign)

    # This part signs any EIP-191-valid message
    signature: SignedMessage = Account().sign_message(
        signable_message=message_to_sign,
        private_key=MINT_SIGNER_PRIVATE_KEY,
    )

    signature_hex_str: str = signature.signature.hex()

    return signature_hex_str
