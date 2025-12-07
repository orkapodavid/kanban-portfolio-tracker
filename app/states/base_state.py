import reflex as rx


class BaseState(rx.State):
    """
    Base state class containing application-wide configuration and user settings.
    """

    available_users: list[str] = [
        "Analyst A",
        "Analyst B",
        "Portfolio Manager",
        "Compliance Officer",
    ]
    theme_mode: str = "light"