"""
Routes for claim API
"""

import ast
import json
from typing import Dict, Union
from fastapi import APIRouter, Request, Body, HTTPException
from .config import URL_PREFIX
from ..claim.claim import claim
from ..claim.typings import ClaimRequest
from ..verification.verification import is_verified
from ..signature.signature import has_valid_signature

router = APIRouter(
    prefix=f"{URL_PREFIX}/claim",
    tags=["claim"],
    responses={404: {"description": "Not found"}},
)


# http://localhost:5000/songadao-rewards-api/claim/?bleh=bleh


def format_error(error: Union[str, Dict[str, str], Exception]):
    """
    Format errors into returnable json
    """

    code = 0
    message = str(error)

    print(str(error))

    try:
        error = ast.literal_eval(str(error))
    except Exception:
        pass

    if isinstance(error, dict) and ("code" in error):
        code = error["code"]

    if isinstance(error, dict) and ("message" in error):
        message = error["message"]

    print(code)
    print(message)

    return {"code": code, "message": message}


def error400(error: Union[str, Dict[str, str], Exception]):
    """
    Handle returning a HTTP 400 error
    """

    raise HTTPException(status_code=400, detail=format_error(error))


@router.get("/")
async def claim_get(req: Request):
    """
    claim API Route (GET)
    """

    payload: Dict[str, str] = dict(req.query_params)

    # Params
    # --------------------------------------------------------------------------

    if "address" not in payload:
        error400("Missing address parameter")

    if "signature" not in payload:
        error400("Missing signature parameter")

    if "nonce" not in payload:
        error400("Missing nonce parameter")

    if "reward_id" not in payload:
        error400("Missing reward id parameter")

    if "reward_data" not in payload:
        error400("Missing reward data parameter")

    # Valid Signature
    # --------------------------------------------------------------------------
    try:
        if (
            has_valid_signature(
                payload["address"], payload["signature"], payload["nonce"]
            )
            is False
        ):
            raise Exception("Address is not allowed to claim")
    except Exception as error:
        error400(error)

    # BrightID Verification
    # --------------------------------------------------------------------------
    try:
        if is_verified(payload["address"]) is False:
            raise Exception("Address is not allowed to claim")
    except Exception as error:
        error400(error)

    # Claim
    # --------------------------------------------------------------------------

    try:
        claim(payload["address"], payload["reward_id"], payload["reward_data"])

        return {"claimed": True}
    except Exception as error:
        error400(error)


# @router.post("/")
# async def claim_post(payload: claimRequest = Body(...)):
#     """
#     claim API Route (POST)
#     """

#     print(payload)

#     # Params
#     # --------------------------------------------------------------------------

#     if "address" not in payload:
#         error400("Missing address parameter")

#     if "traits" not in payload:
#         error400("Missing traits parameter")

#     # Verification
#     # --------------------------------------------------------------------------

#     try:
#         if is_verified(payload["address"]) is False:
#             raise Exception("Address is not allowed to claim")
#     except Exception as error:
#         error400(error)

#     # Input Traits
#     # --------------------------------------------------------------------------

#     input_traits: InputTraits = payload["traits"]
#     print(input_traits)

#     # claim
#     # --------------------------------------------------------------------------

#     try:
#         claim_data = claim(payload["address"], input_traits)

#         return {"data": claim_data}
#     except Exception as error:
#         error400(error)
