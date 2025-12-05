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
    search_query: str = ""
    is_modal_open: bool = False
    pending_move_ticker: str = ""
    pending_move_stage: str = ""
    modal_comment: str = ""
    modal_user: str = "Analyst A"
    available_users: list[str] = [
        "Analyst A",
        "Analyst B",
        "Portfolio Manager",
        "Compliance Officer",
    ]
    is_add_modal_open: bool = False
    new_stock_ticker: str = ""
    new_stock_company: str = ""
    new_stock_stage: str = "Universe"
    is_history_open: bool = False
    history_stock_ticker: str = ""
    history_logs: list[TransitionLog] = []
    stock_to_delete: str = ""

    @rx.var
    def filtered_stocks(self) -> list[Stock]:
        """
        Returns stocks matching the search query.
        """
        if not self.search_query:
            return self.stocks
        query = self.search_query.lower()
        return [
            s
            for s in self.stocks
            if query in s.ticker.lower() or query in s.company_name.lower()
        ]

    @rx.var
    def stocks_by_stage(self) -> dict[str, list[Stock]]:
        """
        Returns filtered stocks organized by stage for easier rendering.
        """
        result = {stage: [] for stage in self.stages}
        for stock in self.filtered_stocks:
            if stock.status in result:
                result[stock.status].append(stock)
        return result

    @rx.event
    def handle_drop(self, item: dict[str, str], new_stage: str):
        """
        Initiates a stock move when a card is dropped. Opens the confirmation modal.
        """
        ticker = item.get("ticker")
        if not ticker:
            return
        stock = next((s for s in self.stocks if s.ticker == ticker), None)
        if stock and stock.status != new_stage:
            self.pending_move_ticker = ticker
            self.pending_move_stage = new_stage
            self.modal_comment = ""
            self.is_modal_open = True

    @rx.event
    def confirm_move(self):
        """
        Executes the pending move after user confirmation.
        """
        if self.pending_move_ticker and self.pending_move_stage:
            self.move_stock(
                self.pending_move_ticker,
                self.pending_move_stage,
                self.modal_comment or "No comment provided",
                self.modal_user,
            )
        self.cancel_move()

    @rx.event
    def cancel_move(self):
        """
        Cancels the pending move and closes the modal.
        """
        self.is_modal_open = False
        self.pending_move_ticker = ""
        self.pending_move_stage = ""
        self.modal_comment = ""

    @rx.event
    def open_add_modal(self):
        self.is_add_modal_open = True
        self.new_stock_ticker = ""
        self.new_stock_company = ""
        self.new_stock_stage = "Universe"

    @rx.event
    def close_add_modal(self):
        self.is_add_modal_open = False

    @rx.event
    def submit_new_stock(self):
        if not self.new_stock_ticker or not self.new_stock_company:
            yield rx.toast.error("Ticker and Company Name are required.")
            return
        if any(
            (s.ticker.upper() == self.new_stock_ticker.upper() for s in self.stocks)
        ):
            yield rx.toast.error(f"Stock {self.new_stock_ticker} already exists.")
            return
        new_stock = Stock(
            ticker=self.new_stock_ticker.upper(),
            company_name=self.new_stock_company,
            status=self.new_stock_stage,
            last_updated=get_utc_now(),
        )
        self.stocks.append(new_stock)
        initial_log = TransitionLog(
            ticker=new_stock.ticker,
            previous_stage="VOID",
            new_stage=self.new_stock_stage,
            timestamp=get_utc_now(),
            user_comment="Initial creation",
            updated_by="System",
        )
        self.logs.append(initial_log)
        yield rx.toast.success(f"Added {new_stock.ticker} to {self.new_stock_stage}")
        self.close_add_modal()

    @rx.event
    def view_history(self, ticker: str):
        self.history_stock_ticker = ticker
        filtered_logs = [log for log in self.logs if log.ticker == ticker]
        filtered_logs.sort(key=lambda x: x.timestamp or get_utc_now(), reverse=True)
        self.history_logs = filtered_logs
        self.is_history_open = True

    @rx.event
    def close_history(self):
        self.is_history_open = False

    @rx.event
    def delete_stock(self, ticker: str):
        self.stocks = [s for s in self.stocks if s.ticker != ticker]
        yield rx.toast.success(f"Deleted stock {ticker}")

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