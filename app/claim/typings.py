"""
Claim typings
"""

from typing import Dict, Union, TypedDict


class ClaimField(TypedDict):
    name: str
    value: str


ClaimFields = list[ClaimField]


class ClaimFieldsInput(TypedDict):
    fields: ClaimFields


class ClaimRequest(TypedDict):
    address: str
    signature: str
    nonce: str
    reward_id: str
    reward_claim_values: ClaimFieldsInput


class ClaimVerificationResponse(TypedDict):
    # tier: Dict[str, Union[str, Dict[str, str]]]
    claimable: bool
