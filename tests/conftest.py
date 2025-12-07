"""
Pytest configuration and fixtures for Kanban Portfolio Tracker tests.
"""
import pytest
from datetime import datetime, timezone, timedelta
from app.states.kanban_state import KanbanState
from app.models import Stock, StateTransitionLog


@pytest.fixture
def clean_state():
    """
    Provides a fresh KanbanState instance with no data.
    
    Returns:
        KanbanState: Clean state instance for testing.
    """
    state = KanbanState()
    state.stocks = []
    state.logs = []
    state.next_stock_id = 1
    state.next_log_id = 1
    return state


@pytest.fixture
def sample_stocks():
    """
    Provides a list of sample Stock objects for testing.
    
    Returns:
        list[Stock]: List of test stock objects.
    """
    now = datetime.now(timezone.utc)
    return [
        Stock(
            id=1,
            ticker="AAPL",
            company_name="Apple Inc.",
            status="Universe",
            last_updated=now,
            current_stage_entered_at=now - timedelta(days=5),
            days_in_stage=5
        ),
        Stock(
            id=2,
            ticker="MSFT",
            company_name="Microsoft Corp.",
            status="Prospects",
            last_updated=now,
            current_stage_entered_at=now - timedelta(days=15),
            days_in_stage=15
        ),
        Stock(
            id=3,
            ticker="GOOGL",
            company_name="Alphabet Inc.",
            status="Ocean",
            last_updated=now,
            current_stage_entered_at=now - timedelta(days=90),
            days_in_stage=90
        ),
    ]


@pytest.fixture
def populated_state(clean_state, sample_stocks):
    """
    Provides a KanbanState pre-populated with sample data.
    
    Args:
        clean_state: Clean state fixture.
        sample_stocks: Sample stocks fixture.
    
    Returns:
        KanbanState: State with sample stocks loaded.
    """
    clean_state.stocks = list(sample_stocks)
    clean_state.next_stock_id = max(s.id for s in sample_stocks) + 1
    return clean_state
