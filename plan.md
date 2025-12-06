# Stock Portfolio Kanban Tracker - Implementation Plan

## Phase 1: Database Models and State Management ✅
- [x] Create Stock model (ticker PK, company_name, status, last_updated)
- [x] Create TransitionLog model (id PK, ticker FK, previous_stage, new_stage, timestamp, user_comment, updated_by)
- [x] Initialize SQLite database with schema and sample data
- [x] Create main application state class with stock loading and filtering by status
- [x] Implement data access methods for reading stocks and writing transition logs

---

## Phase 2: Kanban Board UI and Layout ✅
- [x] Design header with app title, search functionality, and "Add New Stock" button
- [x] Implement 8 Kanban columns (Universe, Prospects, Outreach, Discovery, Live Deal, Execute, Tracker, Ocean)
- [x] Create stock card component displaying ticker and company_name
- [x] Add horizontal scroll layout for board columns
- [x] Style cards with hover states and visual feedback
- [x] Implement search/filter functionality to find stocks by ticker

---

## Phase 3: Drag-and-Drop with Transaction Handling ✅
- [x] Install reflex-enterprise for drag-and-drop components
- [x] Wrap stock cards with draggable component (rxe.dnd.draggable)
- [x] Wrap stage columns with drop target component (rxe.dnd.drop_target)
- [x] Create confirmation modal with user input (updated_by field and comment textarea)
- [x] Implement drop event handler to capture move and trigger modal
- [x] Create backend transaction: update Stock status + insert TransitionLog entry
- [x] Add error handling for database operations
- [x] Implement optimistic UI updates with rollback on failure

---

## Phase 4: Additional Features and Polish ✅
- [x] Add "Add New Stock" modal with form (ticker, company_name, initial stage)
- [x] Implement stock creation with validation
- [x] Add empty state messaging for columns with no stocks
- [x] Create transition history view/modal to display TransitionLog entries for a stock
- [x] Add timestamp formatting and last_updated display
- [x] Implement responsive design for different screen sizes
- [x] Add loading states and error toasts for user feedback
- [x] Add stock count badges to column headers
- [x] Implement delete stock functionality
- [x] Add visual polish and hover effects

---

## Phase 5: State Machine Logic Implementation ✅
- [x] Define strict StageDef enum with display names and associated colors
- [x] Implement stage color mapping: Universe (Gray), Prospects (Blue), Outreach (Indigo), Discovery (Purple), Live Deal (Orange), Execute (Green), Tracker (Teal), Ocean (Slate/Dark Gray)
- [x] Create validate_transition() function with business rules
- [x] Implement forward progress validation (linear stage movement)
- [x] Implement Ocean rule (can move to Ocean from ANY stage)
- [x] Implementation restoration rule (Ocean → Prospects only)
- [x] Add skip validation (warn if skipping >2 stages, but allow it)
- [x] Enhance move_stock() to use validation logic
- [x] Display validation warnings in confirmation modal UI
- [x] Log validation warnings in transition comments

---

## Phase 6: UI Verification and Testing ✅
- [x] Test drag-and-drop functionality across all 8 stages
- [x] Verify confirmation modal appears with correct stock and stage information
- [x] Test "Add New Stock" modal with validation (duplicate tickers, empty fields)
- [x] Verify search functionality filters stocks correctly
- [x] Test transition history modal displays all stock movements
- [x] Verify delete stock functionality with toast notifications
- [x] Test responsive layout and horizontal scrolling
- [x] Verify empty state messaging appears in columns without stocks
- [x] Test state machine validation rules (forward progress, Ocean rule, restoration, skip warnings)
- [x] Verify validation warnings display correctly in modal
- [x] Test stage color coding across all 8 stages

---

## Phase 7: Deal Velocity & Staleness Tracking ✅
- [x] Update Stock model to add `current_stage_entered_at` DateTime field
- [x] Add computed property `days_in_stage` that calculates (now - current_stage_entered_at)
- [x] Update move_stock() to set `current_stage_entered_at` when stage changes
- [x] Update submit_new_stock() to initialize `current_stage_entered_at` for new records
- [x] Initialize `current_stage_entered_at` for existing sample data in initialize_sample_data()
- [x] Update stock card UI to display staleness indicator
- [x] Implement conditional badge formatting: Green (<7 days), Default (7-30 days), Red (>30 days)
- [x] Add visual "Days in Stage" badge to each stock card
- [x] Add "Show Stale Only" filter button in header
- [x] Implement filter toggle to show only stocks with >30 days in stage

---

## Phase 8: UI Verification - Staleness Indicators ✅
- [x] Verify staleness badges display correctly on all cards with proper icons
- [x] Test conditional color formatting (Green Fresh badge, Red Stale badge, Gray default)
- [x] Verify "Show Stale Only" filter button works and displays only stale stocks
- [x] Test that days_in_stage updates correctly when stocks are moved
- [x] Verify empty state messaging when stale filter shows no results

---

## Phase 9: Database Schema Refactor for Data Integrity ✅
- [x] **Stock Model Refactor:**
  - [x] Add `id: int` field as auto-incrementing Primary Key
  - [x] Change `ticker: str` to a standard field with UNIQUE constraint
  - [x] Update Stock model to use `id` as the primary identifier
  - [x] Add data migration logic to populate IDs for existing records
- [x] **TransitionLog Model Refactor:**
  - [x] Add `id: int` field as auto-incrementing Primary Key
  - [x] Change Foreign Key from `ticker: str` to `stock_id: int`
  - [x] Update log creation to reference stock_id instead of ticker
  - [x] Migrate existing logs to use stock_id references
- [x] **State Logic Updates:**
  - [x] Update `move_stock()` to accept `stock_id: int` instead of `ticker: str`
  - [x] Update `delete_stock()` to use stock_id
  - [x] Update `view_history()` to query by stock_id
  - [x] Add `update_ticker()` method to rename tickers without breaking history
  - [x] Update internal state management to track stocks by ID
- [x] **Frontend Updates:**
  - [x] Change draggable component key from `stock.ticker` to `stock.id`
  - [x] Update drop event to send `stock_id` instead of `ticker`
  - [x] Update all UI references to use stock.id for operations
  - [x] Keep ticker display as visual label only
  - [x] Update history modal to fetch by stock_id

---

## Phase 10: UI Verification - Schema Refactor ✅
- [x] Test drag-and-drop with new ID-based system (move stocks between stages)
- [x] Verify stock movements work correctly with stock_id references
- [x] Test ticker uniqueness constraint (try creating duplicate tickers)
- [x] Verify transition history displays correctly after refactor
- [x] Test that all modals and operations use stock_id correctly
- [x] Verify data consistency after stock movements

---

## Phase 11: Deal Detail Modal with Edit Capabilities ✅
- [x] Add state variables for detail modal (is_detail_modal_open, detail_stock_id, active_detail_tab, edit_ticker_value)
- [x] Create open_detail_modal(stock_id) and close_detail_modal() event handlers
- [x] Create save_ticker_edit() event handler that calls update_ticker()
- [x] Create deal_detail_modal() component with tabbed interface
- [x] Implement Overview tab: Display Stock ID (read-only), editable Ticker input field, Rename button, Current Stage, Days in Stage
- [x] Implement Activity Log tab: Render TransitionLog data table with columns (Date, From, To, User, Comment, Type)
- [x] Add conditional formatting for forced transitions (yellow background + rationale display)
- [x] Make stock cards clickable (on_click handler) without interfering with drag functionality
- [x] Wire up modal opening to card click events

---

## Phase 12: Ocean Column Archive View ✅
- [x] Add is_ocean_modal_open state variable for archive view
- [x] Create open_ocean_modal() and close_ocean_modal() event handlers
- [x] Modify droppable_stage_column() to detect if stage == "Ocean"
- [x] For Ocean column: Render single summary card showing "🌊 [Count] Deals in Ocean"
- [x] Make Ocean summary card clickable to open archive modal
- [x] Create ocean_archive_modal() component displaying list of all Ocean stocks
- [x] Allow click-through from archive list to individual deal detail modals
- [x] Ensure Ocean column can still accept drops (remains a drop target)

---

## Phase 13: UI Verification - Deal Detail Modal and Ocean Archive
- [ ] Test clicking stock cards opens detail modal correctly
- [ ] Verify Overview tab displays all stock information accurately (ID, Ticker input, Current Stage, Days in Stage)
- [ ] Test ticker renaming functionality (change ticker, click Rename button, verify update works)
- [ ] Verify Activity Log tab displays all transitions for the stock
- [ ] Test forced transition highlighting (yellow background) in activity log
- [ ] Verify modal closes properly and doesn't interfere with drag-and-drop
- [ ] Test Ocean column shows summary card instead of individual cards
- [ ] Verify Ocean summary card displays correct count
- [ ] Test Ocean summary card click opens archive modal
- [ ] Verify archive modal lists all Ocean stocks
- [ ] Test click-through from archive to detail modal
- [ ] Test search functionality still works with ticker and company_name filtering
