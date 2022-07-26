"""
Routes for claim API
"""

import ast
import json
from typing import Dict, Union
from fastapi import APIRouter, Request, Body, HTTPException
from .config import URL_PREFIX
from ..claim.claim import claim
from ..claim.typings import ClaimRequest, ClaimFieldsInput, ClaimFields
from ..verification.verification import is_verified
from ..signature.signature import has_valid_signature

router = APIRouter(
    prefix=f"{URL_PREFIX}/claim",
    tags=["claim"],
    responses={404: {"description": "Not found"}},
)


# http://localhost:5000/songadao-rewards-api/claim/?address=0xBCD17bC16d53D690Ba29d567E79d41d4a7049451&signature=bleh&nonce=bleh&reward_id=1&reward_claim_values={"fields":[{"name":"testname","value":"testvalue"}]}

# http://localhost:5000/songadao-rewards-api/claim/?address=0xBCD17bC16d53D690Ba29d567E79d41d4a7049451&signature=bleh&nonce=bleh&reward_id=7&reward_claim_values={"fields":[{"name":"testname","value":"testvalue"}]}


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

    if "reward_claim_values" not in payload:
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
            raise Exception("Invalid signature")
    except Exception as error:
        error400(error)

    # BrightID Verification
    # --------------------------------------------------------------------------
    # try:
    #     if is_verified(payload["address"]) is False:
    #         raise Exception("Address is not allowed to claim")
    # except Exception as error:
    #     error400(error)

    # Input Traits
    # --------------------------------------------------------------------------
    try:
        reward_claim_fields_input: ClaimFieldsInput = json.loads(
            payload["reward_claim_values"]
        )
        print(reward_claim_fields_input)
    except Exception:
        error400("Malformed traits parameter")

    # Claim
    # --------------------------------------------------------------------------

    # print(reward_claim_fields_input)
    try:
        claim(
            payload["address"],
            payload["reward_id"],
            reward_claim_fields_input["fields"],
        )

        return {"claimed": True}
    except Exception as error:
        error400(error)


@router.post("/")
async def claim_post(payload: ClaimRequest = Body(...)):
    """
    claim API Route (POST)
    """

    print(payload)

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

    if "reward_claim_values" not in payload:
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
            raise Exception("Invalid signature")
    except Exception as error:
        error400(error)

    # BrightID Verification
    # --------------------------------------------------------------------------
    # try:
    #     if is_verified(payload["address"]) is False:
    #         raise Exception("Address is not allowed to claim")
    # except Exception as error:
    #     error400(error)

    # Input Traits
    # --------------------------------------------------------------------------
    reward_claim_fields_input: ClaimFieldsInput = payload["reward_claim_values"]
    print(reward_claim_fields_input)

    # Claim
    # --------------------------------------------------------------------------

    try:
        claim(
            payload["address"],
            payload["reward_id"],
            reward_claim_fields_input["fields"],
        )

        return {"claimed": True}
    except Exception as error:
        error400(error)
