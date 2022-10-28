import dataclasses
from typing import Optional
import datetime

from django.utils import timezone

@dataclasses.dataclass
class TCredential:
    """Build credential obj"""

    bearer: dataclasses.InitVar[Optional[dict]] = None
    access_token: str = ""
    issued_at: datetime.datetime = timezone.now()
    expires: datetime.datetime = datetime.datetime(
        1, 1, 1, tzinfo=datetime.timezone.utc
    )
    is_expired = True

    def __post_init__(self, bearer: dict) -> None:
        if bearer:
            self.access_token = bearer["access_token"]
            self.expires = self.issued_at + timezone.timedelta(
                seconds=bearer["expires_in"]
            )

    def asdict(self) -> dict:
        return dataclasses.asdict(self)
