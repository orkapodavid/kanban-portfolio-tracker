import reflex as rx
from datetime import datetime, timezone


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Stock(rx.Base):
    """
    Represents a stock in the Kanban portfolio tracker.
    """

    ticker: str
    company_name: str
    status: str
    last_updated: datetime | None = None


class TransitionLog(rx.Base):
    """
    Logs the history of stock movements between stages.
    """

    ticker: str
    previous_stage: str
    new_stage: str
    timestamp: datetime | None = None
    user_comment: str = ""
    updated_by: str = "System"