"""
Comprehensive test suite for Kanban Portfolio Tracker business logic.

Tests cover:
- Transition validation rules
- State movement tracking
- Time calculation accuracy
- Audit trail integrity
"""
import pytest
from datetime import datetime, timezone, timedelta
from app.states.kanban_state import KanbanState
from app.models import Stock, StateTransitionLog


class TestTransitionValidation:
    """Tests for validate_transition business rules."""
    
    def test_valid_forward_progression(self, clean_state):
        """Test that standard forward progression is allowed."""
        # Universe -> Prospects (forward by 1)
        is_valid, is_forceable, message = clean_state.validate_transition(
            "Universe", "Prospects"
        )
        assert is_valid is True
        assert is_forceable is False
        assert message == ""
        
        # Prospects -> Outreach (forward by 1)
        is_valid, is_forceable, message = clean_state.validate_transition(
            "Prospects", "Outreach"
        )
        assert is_valid is True
        assert is_forceable is False
        assert message == ""
    
    def test_valid_ocean_transitions(self, clean_state):
        """Test that any stage can move to Ocean (archive)."""
        stages = ["Universe", "Prospects", "Discovery", "Live Deal", "Execute", "Tracker"]
        
        for stage in stages:
            is_valid, is_forceable, message = clean_state.validate_transition(
                stage, "Ocean"
            )
            assert is_valid is True, f"Moving {stage} -> Ocean should be valid"
            assert is_forceable is False
            assert message == ""
    
    def test_valid_ocean_restoration(self, clean_state):
        """Test that Ocean can only restore to Prospects."""
        # Ocean -> Prospects (valid restoration)
        is_valid, is_forceable, message = clean_state.validate_transition(
            "Ocean", "Prospects"
        )
        assert is_valid is True
        assert is_forceable is False
        assert message == ""
    
    def test_same_stage_rejected(self, clean_state):
        """Test that moving to the same stage is rejected."""
        is_valid, is_forceable, message = clean_state.validate_transition(
            "Universe", "Universe"
        )
        assert is_valid is False
        assert is_forceable is False
        assert "Already in this stage" in message
    
    def test_backward_movement_forceable(self, clean_state):
        """Test that backward movements are forceable but not valid."""
        # Live Deal -> Discovery (backward by 1)
        is_valid, is_forceable, message = clean_state.validate_transition(
            "Live Deal", "Discovery"
        )
        assert is_valid is False
        assert is_forceable is True
        assert "Backward transition" in message
        
        # Execute -> Universe (backward by many)
        is_valid, is_forceable, message = clean_state.validate_transition(
            "Execute", "Universe"
        )
        assert is_valid is False
        assert is_forceable is True
        assert "Backward transition" in message
    
    def test_stage_skipping_forceable(self, clean_state):
        """Test that skipping stages is forceable but not valid."""
        # Universe -> Discovery (skip 2 stages)
        is_valid, is_forceable, message = clean_state.validate_transition(
            "Universe", "Discovery"
        )
        assert is_valid is False
        assert is_forceable is True
        assert "Skipping" in message
        
        # Prospects -> Execute (skip 4 stages)
        is_valid, is_forceable, message = clean_state.validate_transition(
            "Prospects", "Execute"
        )
        assert is_valid is False
        assert is_forceable is True
        assert "Skipping" in message
    
    def test_invalid_ocean_restoration_forceable(self, clean_state):
        """Test that Ocean to non-Prospects stages is forceable."""
        invalid_restorations = ["Universe", "Discovery", "Live Deal", "Execute", "Tracker"]
        
        for stage in invalid_restorations:
            is_valid, is_forceable, message = clean_state.validate_transition(
                "Ocean", stage
            )
            assert is_valid is False, f"Ocean -> {stage} should not be valid"
            assert is_forceable is True, f"Ocean -> {stage} should be forceable"
            assert "restoration" in message.lower() or "Ocean" in message


class TestTrackerAccuracy:
    """Tests for state transition tracking and audit trail."""
    
    def test_move_creates_log_entry(self, populated_state):
        """Test that moving a stock creates exactly one log entry."""
        initial_log_count = len(populated_state.logs)
        stock_id = populated_state.stocks[0].id
        
        # Move stock from Universe to Prospects
        list(populated_state.move_stock(
            stock_id=stock_id,
            new_stage="Prospects",
            comment="Test move",
            user="TestUser"
        ))
        
        # Verify exactly one new log entry
        assert len(populated_state.logs) == initial_log_count + 1
        
        # Verify log content
        new_log = populated_state.logs[-1]
        assert new_log.stock_id == stock_id
        assert new_log.previous_stage == "Universe"
        assert new_log.new_stage == "Prospects"
        assert new_log.user_comment == "Test move"
        assert new_log.updated_by == "TestUser"
        assert new_log.is_forced_transition is False
    
    def test_forced_transition_logged_correctly(self, populated_state):
        """Test that forced transitions are marked in logs."""
        stock_id = populated_state.stocks[1].id  # MSFT in Prospects
        
        # Force a backward move
        list(populated_state.move_stock(
            stock_id=stock_id,
            new_stage="Universe",
            comment="Forced backward",
            user="Admin",
            force_override=True,
            rationale="Testing forced move"
        ))
        
        # Verify forced flag and rationale
        new_log = populated_state.logs[-1]
        assert new_log.is_forced_transition is True
        assert new_log.forced_rationale == "Testing forced move"
        assert new_log.previous_stage == "Prospects"
        assert new_log.new_stage == "Universe"
    
    def test_log_timestamp_accuracy(self, populated_state):
        """Test that log timestamps are current and in UTC."""
        before_move = datetime.now(timezone.utc)
        
        stock_id = populated_state.stocks[0].id
        list(populated_state.move_stock(
            stock_id=stock_id,
            new_stage="Prospects",
            comment="Timestamp test"
        ))
        
        after_move = datetime.now(timezone.utc)
        
        new_log = populated_state.logs[-1]
        assert new_log.timestamp is not None
        assert new_log.timestamp.tzinfo == timezone.utc
        assert before_move <= new_log.timestamp <= after_move
    
    def test_days_in_previous_stage_recorded(self, populated_state):
        """Test that duration in previous stage is captured."""
        stock = populated_state.stocks[0]
        original_days = stock.days_in_stage
        
        list(populated_state.move_stock(
            stock_id=stock.id,
            new_stage="Prospects",
            comment="Duration test"
        ))
        
        new_log = populated_state.logs[-1]
        assert new_log.days_in_previous_stage == original_days


class TestDaysInStageCalculation:
    """Tests for time calculation and staleness detection."""
    
    def test_calculate_days_in_stage_basic(self, clean_state):
        """Test basic days_in_stage calculation."""
        now = datetime.now(timezone.utc)
        stock = Stock(
            id=1,
            ticker="TEST",
            company_name="Test Corp",
            status="Universe",
            current_stage_entered_at=now - timedelta(days=10),
            days_in_stage=0  # Will be calculated
        )
        
        updated_stock = clean_state._calculate_days_in_stage(stock)
        assert updated_stock.days_in_stage == 10
    
    def test_calculate_days_handles_none(self, clean_state):
        """Test that None current_stage_entered_at is handled."""
        stock = Stock(
            id=1,
            ticker="TEST",
            company_name="Test Corp",
            status="Universe",
            current_stage_entered_at=None,
            days_in_stage=0
        )
        
        updated_stock = clean_state._calculate_days_in_stage(stock)
        assert updated_stock.current_stage_entered_at is not None
        assert updated_stock.days_in_stage == 0
    
    def test_calculate_days_timezone_aware(self, clean_state):
        """Test that calculation works with UTC timezone."""
        now = datetime.now(timezone.utc)
        stock = Stock(
            id=1,
            ticker="TEST",
            company_name="Test Corp",
            status="Universe",
            current_stage_entered_at=now - timedelta(days=5, hours=12),
            days_in_stage=0
        )
        
        updated_stock = clean_state._calculate_days_in_stage(stock)
        # 5 full days (12 hours doesn't count as a day)
        assert updated_stock.days_in_stage == 5
    
    def test_days_in_stage_never_negative(self, clean_state):
        """Test that days_in_stage is never negative."""
        now = datetime.now(timezone.utc)
        
        # Even with future timestamp (edge case)
        stock = Stock(
            id=1,
            ticker="TEST",
            company_name="Test Corp",
            status="Universe",
            current_stage_entered_at=now + timedelta(days=1),
            days_in_stage=0
        )
        
        updated_stock = clean_state._calculate_days_in_stage(stock)
        assert updated_stock.days_in_stage >= 0
    
    def test_refresh_stock_ages_updates_all(self, populated_state):
        """Test that refresh_stock_ages updates all stocks."""
        # Manually change days to incorrect values
        for stock in populated_state.stocks:
            stock.days_in_stage = 999
        
        # Refresh should recalculate
        populated_state.refresh_stock_ages()
        
        # Verify all stocks have been recalculated
        for stock in populated_state.stocks:
            assert stock.days_in_stage != 999
            assert stock.days_in_stage >= 0


class TestStateManagement:
    """Tests for overall state management operations."""
    
    def test_move_updates_stock_status(self, populated_state):
        """Test that move_stock updates the stock's status."""
        stock = populated_state.stocks[0]
        original_status = stock.status
        
        list(populated_state.move_stock(
            stock_id=stock.id,
            new_stage="Prospects",
            comment="Status update test"
        ))
        
        assert stock.status == "Prospects"
        assert stock.status != original_status
    
    def test_move_resets_days_in_stage(self, populated_state):
        """Test that moving resets days_in_stage to 0."""
        stock = populated_state.stocks[1]  # MSFT with 15 days
        assert stock.days_in_stage == 15
        
        list(populated_state.move_stock(
            stock_id=stock.id,
            new_stage="Outreach",
            comment="Reset test"
        ))
        
        assert stock.days_in_stage == 0
    
    def test_move_updates_timestamps(self, populated_state):
        """Test that moving updates last_updated and current_stage_entered_at."""
        stock = populated_state.stocks[0]
        old_last_updated = stock.last_updated
        old_stage_entered = stock.current_stage_entered_at
        
        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)
        
        list(populated_state.move_stock(
            stock_id=stock.id,
            new_stage="Prospects",
            comment="Timestamp test"
        ))
        
        assert stock.last_updated > old_last_updated
        assert stock.current_stage_entered_at > old_stage_entered
    
    def test_invalid_stage_rejected(self, populated_state):
        """Test that moving to invalid stage is rejected."""
        stock = populated_state.stocks[0]
        original_status = stock.status
        
        list(populated_state.move_stock(
            stock_id=stock.id,
            new_stage="InvalidStage",
            comment="Should fail"
        ))
        
        # Status should not change
        assert stock.status == original_status
        assert populated_state.last_error == "Invalid stage: InvalidStage"
