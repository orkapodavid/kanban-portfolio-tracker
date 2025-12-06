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
    current_stage_entered_at: datetime | None = None
    days_in_stage: int = 0


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


class StageDef(rx.Base):
    """
    Defines the properties of a Kanban stage including styling.
    """

    name: str
    color: str
    bg_color: str
    border_color: str


STAGES_DATA = [
    {
        "name": "Universe",
        "color": "text-gray-700",
        "bg_color": "bg-gray-50",
        "border_color": "border-gray-200",
    },
    {
        "name": "Prospects",
        "color": "text-blue-700",
        "bg_color": "bg-blue-50",
        "border_color": "border-blue-200",
    },
    {
        "name": "Outreach",
        "color": "text-indigo-700",
        "bg_color": "bg-indigo-50",
        "border_color": "border-indigo-200",
    },
    {
        "name": "Discovery",
        "color": "text-purple-700",
        "bg_color": "bg-purple-50",
        "border_color": "border-purple-200",
    },
    {
        "name": "Live Deal",
        "color": "text-orange-700",
        "bg_color": "bg-orange-50",
        "border_color": "border-orange-200",
    },
    {
        "name": "Execute",
        "color": "text-green-700",
        "bg_color": "bg-green-50",
        "border_color": "border-green-200",
    },
    {
        "name": "Tracker",
        "color": "text-teal-700",
        "bg_color": "bg-teal-50",
        "border_color": "border-teal-200",
    },
    {
        "name": "Ocean",
        "color": "text-slate-700",
        "bg_color": "bg-slate-100",
        "border_color": "border-slate-300",
    },
]