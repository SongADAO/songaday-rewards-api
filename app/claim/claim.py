"""
Handle claiming a reward
"""

import json
import requests
from ..claim.typings import ClaimVerificationResponse, ClaimFields
from .config import (
    CLAIM_VERIFICATION_API,
    REWARD_CLAIM_FROM,
    REWARD_CLAIM_TO,
    SENDGRID_API_KEY,
    POAP_API_KEY,
    POAP_OAUTH_KEY,
    POAP_SECRETS,
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

    # if response_json["tier"]["reward"]["claim_fields"] and reward_claim_fields:
    #     send_claim_email(
    #         response_json["tier"]["name"],
    #         response_json["tier"]["reward"]["offering"][0],
    #         reward_claim_fields,
    #     )

    if response_json["tier"]["reward"]["claim_poap"]:
        claim_poap(address, response_json["tier"]["reward"]["claim_poap"]["eventId"])


def claim_poap(address: str, event_id: str):
    event_id = "56211"

    secrets = json.loads(POAP_SECRETS)

    if event_id not in secrets.keys():
        print(f"Invalid poap id: {address} - {event_id}")
        raise Exception("Invalid poap id")

    secret_code = secrets[event_id]

    # print(secret_code)

    if secret_code == "":
        print(f"Missing poap secret: {address} - {event_id}")
        raise Exception("Missing poap secret")

    url = f"https://api.poap.tech/event/{event_id}/qr-codes"

    payload = {
        "secret_code": secret_code,
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {POAP_OAUTH_KEY}",
        "X-API-Key": POAP_API_KEY,
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response)
    print(response.json())

    if response.ok is False:
        print(f"Poap supply is 0: {address} - {event_id}")
        raise Exception("Poap supply is 0")

    qr_codes = response.json()

    for qr_code in qr_codes:
        if qr_code["claimed"] is False:
            qr_hash = qr_code["qr_hash"]

            url = f"https://api.poap.tech/actions/claim-qr?qr_hash={qr_hash}"

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {POAP_OAUTH_KEY}",
                "X-API-Key": POAP_API_KEY,
            }

            response = requests.get(url, headers=headers)

            print(response)
            print(response.json())

            if response.ok is False:
                print(f"Couldn't find claimable poap: {address} - {event_id}")
                raise Exception("Couldn't find claimable poap")

            claims = response.json()

            if claims["claimed"] is True:
                url = "https://api.poap.tech/actions/claim-qr"

                payload = {
                    "address": address,
                    "qr_hash": claims["qr_hash"],
                    "secret": claims["secret"],
                }

                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {POAP_OAUTH_KEY}",
                    "X-API-Key": POAP_API_KEY,
                }

                response = requests.post(url, json=payload, headers=headers)

                print(response)
                print(response.json())

                # TODO: If error is 'already claimed' just continue the loop.
                # TODO: Make sure the same address can't claim multiple.

                if response.ok is False:
                    print(f"Failed to deliver poap: {address} - {event_id}")
                    raise Exception("Failed to deliver poap")

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
