"""
Handle claiming a reward
"""


def claim(address: str, reward_id: str, reward_data: Dict[str, str]):
    """
    Take a set of traits, generate the image and metadata, and sign it
    """

    # TODO:
    # 1. Get reward info from api.
    #   POAP ID
    #   Collected Fields
    # 2. Check reward api to verify address is valid for claiming reward id.
    # 3. Verify collected data is complete
    # 4. Issue POAP
    # 5. Send email with field data.
