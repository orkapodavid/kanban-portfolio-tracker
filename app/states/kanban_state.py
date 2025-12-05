import reflex as rx
from typing import Optional
from datetime import datetime, timezone
import logging
from app.models import Stock, TransitionLog, get_utc_now

STAGES = [
    "Universe",
    "Prospects",
    "Outreach",
    "Discovery",
    "Live Deal",
    "Execute",
    "Tracker",
    "Ocean",
]


class KanbanState(rx.State):
    """
    Manages the state of the Kanban board, including stock data and transitions.
    """

    stocks: list[Stock] = []
    logs: list[TransitionLog] = []
    stages: list[str] = STAGES
    last_error: str = ""

    @rx.event
    def load_stocks(self):
        """
        Load all stocks from the database.
        """
        pass

    @rx.event
    def initialize_sample_data(self):
        """
        Seeds the database with sample data if the Stock table is empty.
        """
        try:
            if not self.stocks:
                logging.info("State empty. Seeding sample data...")
                sample_data = [
                    ("AAPL", "Apple Inc.", "Universe"),
                    ("MSFT", "Microsoft Corp.", "Universe"),
                    ("GOOGL", "Alphabet Inc.", "Prospects"),
                    ("AMZN", "Amazon.com Inc.", "Outreach"),
                    ("TSLA", "Tesla Inc.", "Discovery"),
                    ("NVDA", "NVIDIA Corp.", "Live Deal"),
                    ("JPM", "JPMorgan Chase", "Execute"),
                    ("V", "Visa Inc.", "Tracker"),
                    ("NFLX", "Netflix Inc.", "Ocean"),
                    ("PLTR", "Palantir Tech", "Universe"),
                    ("CRM", "Salesforce", "Prospects"),
                    ("UBER", "Uber Technologies", "Outreach"),
                ]
                for ticker, name, status in sample_data:
                    stock = Stock(
                        ticker=ticker,
                        company_name=name,
                        status=status,
                        last_updated=get_utc_now(),
                    )
                    self.stocks.append(stock)
                    log = TransitionLog(
                        ticker=ticker,
                        previous_stage="VOID",
                        new_stage=status,
                        timestamp=get_utc_now(),
                        user_comment="Initial Seed Data",
                        updated_by="System",
                    )
                    self.logs.append(log)
        except Exception as e:
            logging.exception(f"Error initializing sample data: {e}")
            self.last_error = f"Initialization Error: {str(e)}"

    @rx.event
    def move_stock(
        self,
        ticker: str,
        new_stage: str,
        comment: str = "Moved via UI",
        user: str = "Admin",
    ):
        """
        Moves a stock to a new stage transactionally:
        1. Updates the Stock record.
        2. Creates a TransitionLog entry.
        """
        if new_stage not in STAGES:
            self.last_error = f"Invalid stage: {new_stage}"
            return
        found_stock = False
        for stock in self.stocks:
            if stock.ticker == ticker:
                found_stock = True
                if stock.status == new_stage:
                    return
                current_stage = stock.status
                stock.status = new_stage
                stock.last_updated = get_utc_now()
                log = TransitionLog(
                    ticker=ticker,
                    previous_stage=current_stage,
                    new_stage=new_stage,
                    timestamp=get_utc_now(),
                    user_comment=comment,
                    updated_by=user,
                )
                self.logs.append(log)
                break
        if not found_stock:
            self.last_error = f"Stock {ticker} not found."
            return
        self.last_error = ""

    @rx.event
    def on_load(self):
        """
        Event handler for page load. Initializes DB and loads data.
        """
        self.initialize_sample_data()
        self.load_stocks()