"""
Handle claiming a reward
"""

import requests
from ..claim.typings import ClaimVerificationResponse, ClaimFields
from .config import (
    CLAIM_VERIFICATION_API,
    REWARD_CLAIM_FROM,
    REWARD_CLAIM_TO,
    SENDGRID_API_KEY,
)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def claim(address: str, reward_id: str, reward_claim_fields: ClaimFields):
    """
    Take a set of traits, generate the image and metadata, and sign it
    """

    verification_url: str = f"{CLAIM_VERIFICATION_API}/reward/{reward_id}/{address}/"
    print(verification_url)

    response: requests.Response = requests.get(
        url=verification_url,
    )
    print(response)

    response_json = response.json()
    print(response_json)

    if response.ok is False:
        print(f"Failed to verify claim: {reward_id} - {address}")
        raise Exception("Failed to verify claim")

    print(response_json["claimable"])

    if "claimable" not in response_json or response_json["claimable"] is not True:
        print(f"Not claimable: {reward_id} - {address}")
        raise Exception("Not claimable")

    if response_json["tier"]["reward"]["claim_fields"] and reward_claim_fields:
        send_claim_email(
            response_json["tier"]["name"],
            response_json["tier"]["reward"]["offering"],
            reward_claim_fields,
        )

    if response_json["tier"]["reward"]["claim_poap"]:
        claim_poap(address, response_json["tier"]["reward"]["claim_poap"])

    # TODO:
    # 1. Get reward info from api.
    #   POAP ID
    #   Collected Fields
    # 2. Check reward api to verify address is valid for claiming reward id.
    # 3. Verify collected data is complete
    # 4. Issue POAP
    # 5. Send email with field data.


def claim_poap(address: str, poap: str):
    # TODO: Claim POAP
    return


def send_claim_email(
    tier_name: str, reward_name: str, reward_claim_fields: ClaimFields
):
    mail_from = REWARD_CLAIM_FROM
    mail_to = REWARD_CLAIM_TO

    msg = MIMEMultipart()
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg["Subject"] = "Song-a-Day Reward Claimed"
    mail_body: str = f"""
A user has just claimed a reward.

Tier:
{tier_name}

Reward:
{reward_name}

Fields:
"""
    for field in reward_claim_fields:
        mail_body = mail_body + field["name"] + ": " + field["value"] + "\n"

    msg.attach(MIMEText(mail_body))

    try:
        server = smtplib.SMTP_SSL("smtp.sendgrid.net", 465)
        server.ehlo()
        server.login("apikey", SENDGRID_API_KEY)
        server.sendmail(mail_from, mail_to, msg.as_string())
        server.close()
        # print(mail_body)
        print("claim email sent")
    except Exception:
        print("failed to send claim email")
