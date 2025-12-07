import reflex as rx
from typing import Optional
from datetime import datetime, timezone, timedelta
import logging
import csv
import io
from app.models import Stock, TransitionLog, StageDef, STAGES_DATA, get_utc_now
from app.states.base_state import BaseState


class KanbanState(BaseState):
    """
    Manages the state of the Kanban board, including stock data and transitions.
    Inherits from BaseState for shared app configuration.
    """

    stocks: list[Stock] = []
    logs: list[TransitionLog] = []
    stage_defs: list[StageDef] = [StageDef(**data) for data in STAGES_DATA]
    last_error: str = ""
    search_query: str = ""
    show_stale_only: bool = False
    is_modal_open: bool = False
    pending_move_ticker: str = ""
    pending_move_stock_id: int = -1
    pending_move_stage: str = ""
    transition_warning: str = ""
    modal_comment: str = ""
    modal_user: str = "Analyst A"
    is_force_modal_open: bool = False
    force_rationale: str = ""
    is_add_modal_open: bool = False
    new_stock_ticker: str = ""
    new_stock_company: str = ""
    new_stock_stage: str = "Universe"
    is_detail_modal_open: bool = False
    detail_stock_id: int = -1
    active_detail_tab: str = "overview"
    is_ocean_modal_open: bool = False
    next_stock_id: int = 1
    next_log_id: int = 1
    is_mobile_menu_open: bool = False
    mobile_active_stage: str = "Universe"

    @rx.var
    def current_detail_stock(self) -> Stock:
        """
        Returns the stock currently being viewed in the detail modal.

        Returns:
            Stock: The stock object or a default empty stock if not found.
        """
        return next(
            (s for s in self.stocks if s.id == self.detail_stock_id),
            Stock(id=-1, ticker="", company_name="", status=""),
        )

    @rx.var
    def current_detail_logs(self) -> list[TransitionLog]:
        """
        Returns history logs for the detailed stock.

        Returns:
            list[TransitionLog]: List of transition logs sorted by timestamp descending.
        """
        logs = [log for log in self.logs if log.stock_id == self.detail_stock_id]
        return sorted(logs, key=lambda x: x.timestamp or get_utc_now(), reverse=True)

    @rx.var
    def ocean_stocks(self) -> list[Stock]:
        """
        Returns all stocks in the Ocean stage.

        Returns:
            list[Stock]: List of stocks in 'Ocean' status.
        """
        return [s for s in self.stocks if s.status == "Ocean"]

    @rx.var
    def stages(self) -> list[str]:
        """
        Returns list of stage names for compatibility and iteration.

        Returns:
            list[str]: List of stage names.
        """
        return [s.name for s in self.stage_defs]

    @rx.var
    def filtered_stocks(self) -> list[Stock]:
        """
        Returns stocks matching the search query and filters.

        Returns:
            list[Stock]: List of filtered stock objects.
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
    async def export_to_csv(self):
        """
        Generates and downloads a CSV export of the current filtered stock list.
        """
        try:
            yield rx.toast.info("Generating CSV export...")
            output = io.StringIO()
            writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                [
                    "Stock ID",
                    "Ticker",
                    "Company Name",
                    "Current Stage",
                    "Days in Stage",
                    "Last Updated (UTC)",
                ]
            )
            for stock in self.filtered_stocks:
                last_updated_str = (
                    stock.last_updated.strftime("%Y-%m-%d %H:%M")
                    if stock.last_updated
                    else ""
                )
                writer.writerow(
                    [
                        stock.id,
                        stock.ticker,
                        stock.company_name,
                        stock.status,
                        stock.days_in_stage,
                        last_updated_str,
                    ]
                )
            csv_content = output.getvalue()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kanban_export_{timestamp}.csv"
            yield rx.download(data=csv_content, filename=filename)
            yield rx.toast.success("Export ready for download.")
        except Exception as e:
            logging.exception(f"Export failed: {e}")
            yield rx.toast.error(f"Export failed: {str(e)}")

    @rx.event
    def toggle_stale_filter(self):
        """Toggles the stale stock filter on/off."""
        self.show_stale_only = not self.show_stale_only

    @rx.event
    def toggle_mobile_menu(self):
        """Toggles the visibility of the mobile navigation menu."""
        self.is_mobile_menu_open = not self.is_mobile_menu_open

    @rx.event
    def set_mobile_active_stage(self, stage_name: str):
        """
        Sets the currently active stage for mobile view.

        Args:
            stage_name (str): The name of the stage to display.
        """
        self.mobile_active_stage = stage_name

    @rx.event
    def set_search_query(self, query: str):
        """
        Sets the search query for filtering stocks.

        Args:
            query (str): The search text.
        """
        self.search_query = query

    @rx.event
    def clear_filters(self):
        """Clears all active filters (search and stale)."""
        self.search_query = ""
        self.show_stale_only = False

    @rx.var
    def stocks_by_stage(self) -> dict[str, list[Stock]]:
        """
        Returns filtered stocks organized by stage for easier rendering.

        Returns:
            dict[str, list[Stock]]: Dictionary mapping stage names to lists of stocks.
        """
        result = {stage: [] for stage in self.stages}
        for stock in self.filtered_stocks:
            if stock.status in result:
                result[stock.status].append(stock)
        return result

    @rx.event
    def validate_transition(
        self, current_stage: str, new_stage: str
    ) -> tuple[bool, bool, str]:
        """
        Validates if a transition is allowed based on business rules.

        Args:
            current_stage (str): The current stage of the stock.
            new_stage (str): The target stage.

        Returns:
            tuple[bool, bool, str]: (is_valid, is_forceable, message)
        """
        if current_stage == new_stage:
            return (False, False, "Already in this stage.")
        try:
            current_idx = next(
                (i for i, s in enumerate(self.stage_defs) if s.name == current_stage)
            )
            new_idx = next(
                (i for i, s in enumerate(self.stage_defs) if s.name == new_stage)
            )
        except StopIteration as e:
            logging.exception(f"Error: {e}")
            return (False, False, "Invalid stage definition.")
        if new_stage == "Ocean":
            return (True, False, "")
        if current_stage == "Ocean":
            if new_stage == "Prospects":
                return (True, False, "")
            return (
                False,
                True,
                "Non-standard restoration (Ocean only restores to Prospects).",
            )
        if new_idx == current_idx + 1:
            return (True, False, "")
        if new_idx < current_idx:
            return (False, True, "Backward transition detected.")
        if new_idx > current_idx + 1:
            return (False, True, f"Skipping {new_idx - current_idx - 1} stages.")
        return (False, True, "Unknown transition pattern.")

    @rx.event
    def handle_drop(self, item: dict[str, str | int], new_stage: str):
        """
        Initiates a stock move when a card is dropped. Opens the confirmation modal or force modal.

        Args:
            item (dict): The dropped item data containing 'stock_id'.
            new_stage (str): The name of the stage dropped onto.
        """
        stock_id = item.get("stock_id")
        if not stock_id:
            return
        try:
            stock_id = int(stock_id)
        except (ValueError, TypeError) as e:
            logging.exception(f"Error converting stock_id to int: {e}")
            return
        stock = next((s for s in self.stocks if s.id == stock_id), None)
        if not stock:
            return
        is_valid, is_forceable, message = self.validate_transition(
            stock.status, new_stage
        )
        if not is_valid and (not is_forceable):
            yield rx.toast.error(f"Move not allowed: {message}")
            return
        self.pending_move_stock_id = stock_id
        self.pending_move_ticker = stock.ticker
        self.pending_move_stage = new_stage
        self.transition_warning = message
        if not is_valid and is_forceable:
            self.force_rationale = ""
            self.is_force_modal_open = True
        else:
            self.modal_comment = ""
            self.is_modal_open = True

    @rx.event
    def confirm_move(self):
        """
        Executes the pending move after user confirmation.
        """
        if self.pending_move_stock_id != -1 and self.pending_move_stage:
            final_comment = self.modal_comment or "No comment provided"
            if self.transition_warning:
                final_comment = f"[{self.transition_warning}] {final_comment}"
            self.move_stock(
                self.pending_move_stock_id,
                self.pending_move_stage,
                final_comment,
                self.modal_user,
                force_override=False,
            )
        self.cancel_move()

    @rx.event
    def confirm_force_move(self):
        """
        Executes a forced transition.
        """
        if not self.force_rationale:
            yield rx.toast.error("Rationale is required for forced transitions.")
            return
        if self.pending_move_stock_id != -1 and self.pending_move_stage:
            self.move_stock(
                self.pending_move_stock_id,
                self.pending_move_stage,
                self.force_rationale,
                self.modal_user,
                force_override=True,
                rationale=self.force_rationale,
            )
        self.close_force_modal()

    @rx.event
    def cancel_move(self):
        """
        Cancels the pending move and closes the modal.
        """
        self.is_modal_open = False
        self.pending_move_stock_id = -1
        self.pending_move_ticker = ""
        self.pending_move_stage = ""
        self.modal_comment = ""
        self.transition_warning = ""

    @rx.event
    def close_force_modal(self):
        """Closes the force transition modal and resets state."""
        self.is_force_modal_open = False
        self.pending_move_stock_id = -1
        self.pending_move_ticker = ""
        self.pending_move_stage = ""
        self.force_rationale = ""
        self.transition_warning = ""

    @rx.event
    def open_add_modal(self):
        """Opens the add stock modal and resets form fields."""
        self.is_add_modal_open = True
        self.new_stock_ticker = ""
        self.new_stock_company = ""
        self.new_stock_stage = "Universe"

    @rx.event
    def close_add_modal(self):
        """Closes the add stock modal."""
        self.is_add_modal_open = False

    @rx.event
    def open_detail_modal(self, stock_id: int, tab: str = "overview"):
        """
        Opens the detail modal for a specific stock.

        Args:
            stock_id (int): ID of the stock to view.
            tab (str, optional): Initial tab to show ('overview' or 'activity'). Defaults to "overview".
        """
        self.detail_stock_id = stock_id
        self.active_detail_tab = tab
        self.is_detail_modal_open = True

    @rx.event
    def close_detail_modal(self):
        """Closes the detail modal."""
        self.is_detail_modal_open = False
        self.detail_stock_id = -1

    @rx.event
    def set_active_detail_tab(self, value: str):
        """
        Sets the active tab in the detail modal.

        Args:
            value (str): The tab identifier.
        """
        self.active_detail_tab = value

    @rx.event
    def open_ocean_modal(self):
        """Opens the Ocean archive modal."""
        self.is_ocean_modal_open = True

    @rx.event
    def close_ocean_modal(self):
        """Closes the Ocean archive modal."""
        self.is_ocean_modal_open = False

    @rx.event
    def set_new_stock_ticker(self, value: str):
        """Sets the ticker for the new stock form."""
        self.new_stock_ticker = value

    @rx.event
    def set_new_stock_company(self, value: str):
        """Sets the company name for the new stock form."""
        self.new_stock_company = value

    @rx.event
    def set_new_stock_stage(self, value: str):
        """Sets the stage for the new stock form."""
        self.new_stock_stage = value

    @rx.event
    def set_modal_user(self, value: str):
        """Sets the user performing the action in the confirmation modal."""
        self.modal_user = value

    @rx.event
    def set_modal_comment(self, value: str):
        """Sets the comment in the confirmation modal."""
        self.modal_comment = value

    @rx.event
    def set_force_rationale(self, value: str):
        """Sets the rationale in the force transition modal."""
        self.force_rationale = value

    @rx.event
    def submit_new_stock(self):
        """
        Creates a new stock entity based on form data.
        """
        if not self.new_stock_ticker or not self.new_stock_company:
            yield rx.toast.error("Ticker and Company Name are required.")
            return
        if any(
            (s.ticker.upper() == self.new_stock_ticker.upper() for s in self.stocks)
        ):
            yield rx.toast.error(f"Stock {self.new_stock_ticker} already exists.")
            return
        new_id = self.next_stock_id
        self.next_stock_id += 1
        new_stock = Stock(
            id=new_id,
            ticker=self.new_stock_ticker.upper(),
            company_name=self.new_stock_company,
            status=self.new_stock_stage,
            last_updated=get_utc_now(),
            current_stage_entered_at=get_utc_now(),
            days_in_stage=0,
        )
        self.stocks.append(new_stock)
        new_log_id = self.next_log_id
        self.next_log_id += 1
        initial_log = TransitionLog(
            id=new_log_id,
            stock_id=new_id,
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
    def delete_stock(self, stock_id: int):
        """
        Deletes a stock from the board.

        Args:
            stock_id (int): ID of the stock to delete.
        """
        stock = next((s for s in self.stocks if s.id == stock_id), None)
        if stock:
            self.stocks = [s for s in self.stocks if s.id != stock_id]
            if self.is_detail_modal_open and self.detail_stock_id == stock_id:
                self.is_detail_modal_open = False
                self.detail_stock_id = -1
            yield rx.toast.success(f"Deleted stock {stock.ticker}")

    @rx.event
    def load_stocks(self):
        """
        Load all stocks from the database (simulated).
        """
        self.refresh_stock_ages()

    def _calculate_days_in_stage(self, stock: Stock) -> Stock:
        """
        Helper to update the days_in_stage based on current time.

        Args:
            stock (Stock): The stock to update.

        Returns:
            Stock: The updated stock object.
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
                    s_id = self.next_stock_id
                    self.next_stock_id += 1
                    l_id = self.next_log_id
                    self.next_log_id += 1
                    stock = Stock(
                        id=s_id,
                        ticker=ticker,
                        company_name=name,
                        status=status,
                        last_updated=entered_at,
                        current_stage_entered_at=entered_at,
                        days_in_stage=days_stale,
                    )
                    self.stocks.append(stock)
                    log = TransitionLog(
                        id=l_id,
                        stock_id=s_id,
                        ticker=ticker,
                        previous_stage="VOID",
                        new_stage=status,
                        timestamp=entered_at,
                        user_comment="Initial Seed Data",
                        updated_by="System",
                        days_in_previous_stage=0,
                    )
                    self.logs.append(log)
            else:
                migrated = False
                for stock in self.stocks:
                    if stock.id == 0:
                        stock.id = self.next_stock_id
                        self.next_stock_id += 1
                        migrated = True
                if migrated:
                    self.stocks = list(self.stocks)
        except Exception as e:
            logging.exception(f"Error initializing sample data: {e}")
            self.last_error = f"Initialization Error: {str(e)}"

    @rx.event
    def move_stock(
        self,
        stock_id: int,
        new_stage: str,
        comment: str = "Moved via UI",
        user: str = "Admin",
        force_override: bool = False,
        rationale: str = "",
    ):
        """
        Moves a stock to a new stage transactionally.

        Args:
            stock_id (int): ID of stock to move.
            new_stage (str): Destination stage.
            comment (str): User comment for the logs.
            user (str): Username performing the action.
            force_override (bool): Flag if this was a forced move.
            rationale (str): Reason for forcing if applicable.
        """
        if new_stage not in self.stages:
            self.last_error = f"Invalid stage: {new_stage}"
            return
        found_stock = False
        for stock in self.stocks:
            if stock.id == stock_id:
                found_stock = True
                if stock.status == new_stage:
                    return
                current_stage = stock.status
                duration = stock.days_in_stage
                stock.status = new_stage
                stock.last_updated = get_utc_now()
                stock.current_stage_entered_at = get_utc_now()
                stock.days_in_stage = 0
                stock.is_forced = force_override
                l_id = self.next_log_id
                self.next_log_id += 1
                log = TransitionLog(
                    id=l_id,
                    stock_id=stock.id,
                    ticker=stock.ticker,
                    previous_stage=current_stage,
                    new_stage=new_stage,
                    timestamp=get_utc_now(),
                    user_comment=comment,
                    updated_by=user,
                    days_in_previous_stage=duration,
                    is_forced_transition=force_override,
                    forced_rationale=rationale,
                )
                self.logs.append(log)
                if force_override:
                    yield rx.toast.warning(f"Forced move: {stock.ticker} → {new_stage}")
                else:
                    yield rx.toast.success(f"Moved {stock.ticker} to {new_stage}")
                break
        self.stocks = list(self.stocks)
        if not found_stock:
            self.last_error = f"Stock ID {stock_id} not found."
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