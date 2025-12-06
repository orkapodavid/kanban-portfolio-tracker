import reflex as rx
from typing import Optional
from datetime import datetime, timezone, timedelta
import logging
from app.models import Stock, TransitionLog, StageDef, STAGES_DATA, get_utc_now


class KanbanState(rx.State):
    """
    Manages the state of the Kanban board, including stock data and transitions.
    """

    stocks: list[Stock] = []
    logs: list[TransitionLog] = []
    stage_defs: list[StageDef] = [StageDef(**data) for data in STAGES_DATA]
    last_error: str = ""
    search_query: str = ""
    is_modal_open: bool = False
    pending_move_ticker: str = ""
    pending_move_stage: str = ""
    transition_warning: str = ""
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
    show_stale_only: bool = False

    @rx.var
    def stages(self) -> list[str]:
        """Returns list of stage names for compatibility and iteration."""
        return [s.name for s in self.stage_defs]

    @rx.var
    def filtered_stocks(self) -> list[Stock]:
        """
        Returns stocks matching the search query and filters.
        """
        stocks = self.stocks
        if self.search_query:
            query = self.search_query.lower()
            stocks = [
                s
                for s in stocks
                if query in s.ticker.lower() or query in s.company_name.lower()
            ]
        if self.show_stale_only:
            stocks = [s for s in stocks if s.days_in_stage > 30]
        return stocks

    @rx.event
    def toggle_stale_filter(self):
        self.show_stale_only = not self.show_stale_only

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
    def validate_transition(
        self, current_stage: str, new_stage: str
    ) -> tuple[bool, str]:
        """
        Validates if a transition is allowed based on business rules.
        Returns: (is_valid, message)
        """
        if current_stage == new_stage:
            return (False, "Already in this stage.")
        try:
            current_idx = next(
                (i for i, s in enumerate(self.stage_defs) if s.name == current_stage)
            )
            new_idx = next(
                (i for i, s in enumerate(self.stage_defs) if s.name == new_stage)
            )
        except StopIteration as e:
            logging.exception(f"Error: {e}")
            return (False, "Invalid stage definition.")
        if new_stage == "Ocean":
            return (True, "")
        if current_stage == "Ocean":
            if new_stage == "Prospects":
                return (True, "")
            return (False, "Items in Ocean can only be restored to Prospects.")
        if new_idx < current_idx:
            return (
                False,
                "Cannot move stocks backwards (unless restoring from Ocean).",
            )
        if new_idx - current_idx > 2:
            return (
                True,
                f"Warning: You are skipping {new_idx - current_idx} stages. Please verify.",
            )
        return (True, "")

    @rx.event
    def handle_drop(self, item: dict[str, str], new_stage: str):
        """
        Initiates a stock move when a card is dropped. Opens the confirmation modal.
        """
        ticker = item.get("ticker")
        if not ticker:
            return
        stock = next((s for s in self.stocks if s.ticker == ticker), None)
        if not stock:
            return
        is_valid, message = self.validate_transition(stock.status, new_stage)
        if not is_valid:
            yield rx.toast.error(f"Move failed: {message}")
            return
        if stock.status != new_stage:
            self.pending_move_ticker = ticker
            self.pending_move_stage = new_stage
            self.modal_comment = ""
            self.transition_warning = message
            self.is_modal_open = True

    @rx.event
    def confirm_move(self):
        """
        Executes the pending move after user confirmation.
        """
        if self.pending_move_ticker and self.pending_move_stage:
            final_comment = self.modal_comment or "No comment provided"
            if self.transition_warning:
                final_comment = f"[{self.transition_warning}] {final_comment}"
            self.move_stock(
                self.pending_move_ticker,
                self.pending_move_stage,
                final_comment,
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
        self.transition_warning = ""

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
            current_stage_entered_at=get_utc_now(),
            days_in_stage=0,
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
        self.refresh_stock_ages()

    def _calculate_days_in_stage(self, stock: Stock) -> Stock:
        """
        Helper to update the days_in_stage based on current time.
        """
        if stock.current_stage_entered_at is None:
            stock.current_stage_entered_at = get_utc_now()
        delta = get_utc_now() - stock.current_stage_entered_at
        stock.days_in_stage = max(0, delta.days)
        return stock

    @rx.event
    def refresh_stock_ages(self):
        """
        Recalculates days_in_stage for all stocks to ensure staleness is accurate.
        Acts as a migration for records with missing timestamps.
        """
        self.stocks = [self._calculate_days_in_stage(s) for s in self.stocks]

    @rx.event
    def initialize_sample_data(self):
        """
        Seeds the database with sample data if the Stock table is empty.
        """
        try:
            if not self.stocks:
                logging.info("State empty. Seeding sample data...")
                sample_data = [
                    ("AAPL", "Apple Inc.", "Universe", 2),
                    ("MSFT", "Microsoft Corp.", "Universe", 45),
                    ("GOOGL", "Alphabet Inc.", "Prospects", 15),
                    ("AMZN", "Amazon.com Inc.", "Outreach", 5),
                    ("TSLA", "Tesla Inc.", "Discovery", 35),
                    ("NVDA", "NVIDIA Corp.", "Live Deal", 1),
                    ("JPM", "JPMorgan Chase", "Execute", 60),
                    ("V", "Visa Inc.", "Tracker", 20),
                    ("NFLX", "Netflix Inc.", "Ocean", 90),
                    ("PLTR", "Palantir Tech", "Universe", 0),
                    ("CRM", "Salesforce", "Prospects", 8),
                    ("UBER", "Uber Technologies", "Outreach", 3),
                ]
                for ticker, name, status, days_stale in sample_data:
                    entered_at = get_utc_now() - timedelta(days=days_stale)
                    stock = Stock(
                        ticker=ticker,
                        company_name=name,
                        status=status,
                        last_updated=entered_at,
                        current_stage_entered_at=entered_at,
                        days_in_stage=days_stale,
                    )
                    self.stocks.append(stock)
                    log = TransitionLog(
                        ticker=ticker,
                        previous_stage="VOID",
                        new_stage=status,
                        timestamp=entered_at,
                        user_comment="Initial Seed Data",
                        updated_by="System",
                        days_in_previous_stage=0,
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
        if new_stage not in self.stages:
            self.last_error = f"Invalid stage: {new_stage}"
            return
        found_stock = False
        for stock in self.stocks:
            if stock.ticker == ticker:
                found_stock = True
                if stock.status == new_stage:
                    return
                current_stage = stock.status
                duration = stock.days_in_stage
                stock.status = new_stage
                stock.last_updated = get_utc_now()
                stock.current_stage_entered_at = get_utc_now()
                stock.days_in_stage = 0
                log = TransitionLog(
                    ticker=ticker,
                    previous_stage=current_stage,
                    new_stage=new_stage,
                    timestamp=get_utc_now(),
                    user_comment=comment,
                    updated_by=user,
                    days_in_previous_stage=duration,
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
        self.refresh_stock_ages()