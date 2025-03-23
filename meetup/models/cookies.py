from dataclasses import dataclass
from typing import TypedDict


BaseCookies = TypedDict(
        "BaseCookies", {
            'MEETUP_BROWSER_ID': str,
            'MEETUP_TRACK': str,
            'LOGGED_OUT_HOMEPAGE_SEGMENTATION': str,
            '__stripe_mid': str,
            'MEETUP_SESSION': str,
            '__meetup_auth_access_token': str,
            'ab.storage.deviceId.4e505175-14eb-44b5-b07f-b0edb6050714': str,
            'ab.storage.userId.4e505175-14eb-44b5-b07f-b0edb6050714': str,
            'ab.storage.sessionId.4e505175-14eb-44b5-b07f-b0edb6050714': str,
            '__Host-NEXT_MEETUP_CSRF': str,
            'SIFT_SESSION_ID': str,
            'MEETUP_CSRF': str,
            'enable_fundraising_pledge_banner_show': str,
            'MEETUP_MEMBER_LOCATION': str,
            '__stripe_sid': str,
            "memberId": int,
            "isSpooner": str,
            "smdsd": str
        },
        total=False
    )


