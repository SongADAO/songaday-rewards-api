"""
Claim typings
"""

import io
from typing import Dict, Literal, TypedDict


class ClaimRequest(TypedDict):
    address: str
    signature: str
    nonce: str
    reward_id: str
    reward_data: Dict[str, str]
